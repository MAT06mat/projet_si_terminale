from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import (
    ListProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty,
    StringProperty,
)
from kivy.input.motionevent import MotionEvent
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from math import pi

from ui.cubies import Cubie, PROJECTION_MATRIX, get_rotation_matrix
from imports import solver

CN = solver.CubeNotation


class RubiksCube(Widget, solver.Cube):
    angle = ListProperty([pi / 4, pi / 4, 0])
    """
    List of angles for rotation around the x, y, and z axes.
    """

    scale = NumericProperty(40)
    """
    Scale factor for the size of the cube.
    """

    border = NumericProperty(2)
    """
    Width of the border lines around each face.
    """

    allow_rotation = BooleanProperty(True)
    """
    Boolean to allow or disallow rotation of the cube.
    """

    max_y_rotation = BooleanProperty(False)
    """
    Boolean to limit the maximum rotation around the y-axis.
    """

    background_color = ColorProperty((0.9, 0.9, 0.9, 1))
    """
    Background color of the widget, in the format (r, g, b, a).
    """

    border_color = ColorProperty((0.1, 0.1, 0.1, 1))
    """
    Color of the border lines around each face, in the format (r, g, b, a).
    """

    frame_rate = NumericProperty(1 / 60)
    """
    Frame rate for updating the cube.
    """

    faces_colors = {
        CN.U: (1, 1, 1),
        CN.R: (1, 0.35, 0),
        CN.F: (0, 0.27, 0.68),
        CN.D: (1, 0.84, 0),
        CN.L: (0.72, 0.07, 0.20),
        CN.B: (0, 0.61, 0.28),
    }
    """
    Colors of each face of the cube.
    """

    cube_update = BooleanProperty(True)
    """
    Control when the cube is updated.
    """

    _cube_string = StringProperty("")
    _last_touch_pos = None
    _turn_face = None
    _turn_angle = [0, 0, 0]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._cubies = [
            Cubie(self, r_pos=(2 * x, 2 * y, 2 * z))
            for x in range(-1, 2)
            for y in range(-1, 2)
            for z in range(-1, 2)
            if (x, y, z) != (0, 0, 0)
        ]
        self._center_cubies: list[Cubie] = []
        for cubie in self._cubies:
            if len(cubie.faces_to_render) == 1:
                self._center_cubies.append(cubie)
        self._cube_update()
        self.bind(cube_update=self._cube_update)
        self.bind(_cube_string=self.update_colors)
        self._turn_animation = Animation(_turn_angle=[0, 0, 0], d=0.5, t="in_out_sine")

    def _cube_update(self, *args):
        if self.cube_update:
            self._update_event = Clock.schedule_interval(
                self.update_cube, self.frame_rate
            )
        else:
            self._update_event.cancel()

    def _is_point_in_triangle(self, px, py, ax, ay, bx, by, cx, cy) -> bool:
        """
        Check if a point (px, py) is inside a triangle defined by points (ax, ay), (bx, by), and (cx, cy).
        Uses barycentric coordinates to determine if the point is inside the triangle.
        """
        # Calculate barycentric coordinates to check if the point is inside the triangle
        denominator = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if denominator == 0:
            return False  # Degenerate triangle

        a = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / denominator
        b = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / denominator
        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def _is_touch_inside_face(self, touch_pos, face_points) -> bool:
        """
        Check if a touch position is inside a face defined by 4 points.
        Decomposes the face into two triangles and checks if the touch position is inside either triangle.
        """
        x, y = touch_pos

        # Decompose the face into two triangles
        (ax, ay), (bx, by), (cx, cy), (dx, dy) = face_points

        # Check if the point is inside either triangle
        return self._is_point_in_triangle(
            x, y, ax, ay, bx, by, cx, cy
        ) or self._is_point_in_triangle(x, y, ax, ay, cx, cy, dx, dy)

    def on_touch_down(self, touch: MotionEvent):
        """
        Handle touch down events.
        """
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self._last_touch_pos = touch.pos
            self._last_face_touch = None
            # Detect if a face is touched
            for cubie in self._cubies:
                if cubie.r_pos.count(0) != 2:
                    continue
                for face in cubie.faces_to_render:
                    if not cubie.is_face_visible(face):
                        continue
                    points = cubie.get_points(face).copy()
                    center = (points[0] + points[2]) / 2
                    face_coords = [None, None, None, None]
                    for i, p in enumerate(points):
                        face_coords[i] = center + 3 * (p - center)
                    if self._is_touch_inside_face(touch.pos, face_coords):
                        self._last_face_touch = face
            Window.set_system_cursor("hand")
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch: MotionEvent):
        """
        Handle touch move events.
        """
        if touch.grab_current is self and self.allow_rotation:
            dx = touch.pos[0] - self._last_touch_pos[0]
            dy = touch.pos[1] - self._last_touch_pos[1]

            mult = self.get_mult()

            self.angle[0] -= dy / mult * 0.3
            if self.max_y_rotation:
                if self.angle[0] < pi:
                    self.angle[0] = min(self.angle[0], pi / 2)
                else:
                    self.angle[0] = max(self.angle[0], 3 * pi / 2)
            if pi / 2 < self.angle[0] < 3 * pi / 2:
                self.angle[1] -= dx / mult * 0.3
            else:
                self.angle[1] += dx / mult * 0.3
            self.angle[0] %= 2 * pi
            self.angle[1] %= 2 * pi
            self.angle[2] %= 2 * pi

            self._last_touch_pos = touch.pos
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch: MotionEvent):
        """
        Handle touch up events.
        """
        if touch.grab_current is self:
            touch.ungrab(self)
            if (
                self._last_face_touch
                and (touch.time_end - touch.time_start) < 0.3
                and touch.dpos == (0, 0)
                and (not self._turn_face or self._turn_face == self._last_face_touch)
            ):
                self.turn(self._last_face_touch)
            Window.set_system_cursor("arrow")
            return True
        return super().on_touch_up(touch)

    def turn(self, move):
        face = move[0]
        for cubie in self._center_cubies:
            if cubie.faces_to_render == face:
                self._turn_face = face
                match face:
                    case CN.B:
                        self._turn_angle[2] += pi / 2
                    case CN.F:
                        self._turn_angle[2] -= pi / 2
                    case CN.U:
                        self._turn_angle[1] += pi / 2
                    case CN.D:
                        self._turn_angle[1] -= pi / 2
                    case CN.L:
                        self._turn_angle[0] += pi / 2
                    case CN.R:
                        self._turn_angle[0] -= pi / 2
                self._turn_animation.start(self)
        return super().turn(move)

    def update_colors(self, *args) -> None:
        for cubie in self._cubies:
            cubie.update_colors()

    def get_mult(self):
        if self.width > self.height:
            size = self.height
        else:
            size = self.width

        return self.scale / 600 * size

    def update_cube(self, *args) -> None:
        """
        Update the cube's rotation and render it.
        """
        rotation_matrix = get_rotation_matrix(self.angle)
        mult = self.get_mult()

        # Combine rotation and projection matrices
        combined_matrix = PROJECTION_MATRIX * rotation_matrix

        self.canvas.clear()
        with self.canvas:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)
            # Render cubies
            if not self._turn_face:
                for cubie in self._cubies:
                    cubie.render(combined_matrix, mult)
            else:
                for cubie in self._cubies:
                    if self._turn_face not in cubie.faces_to_render:
                        cubie.render(combined_matrix, mult)
                # Render black face if there are an animation
                for cubie in self._center_cubies:
                    if (
                        self._turn_face == cubie.faces_to_render
                        and cubie.is_face_visible(self._turn_face)
                    ):
                        Color(*self.border_color)
                        # Update projected points
                        for i, point in enumerate(cubie.points):
                            cubie.projected_points[i] = cubie.project_point(
                                point,
                                tuple(-i / 3 for i in cubie.r_pos),
                                combined_matrix,
                                mult * 3,
                            )
                            cubie.draw_face(cubie.faces_to_render)
                # Update combined matrix for animation
                combined_matrix = combined_matrix * get_rotation_matrix(
                    self._turn_angle
                )
                # Render cubies with animation after others
                for cubie in self._cubies:
                    if self._turn_face in cubie.faces_to_render:
                        cubie.render(combined_matrix, mult)
                if self._turn_angle == [0, 0, 0]:
                    self._turn_face = None

    def from_string(self, patternstring, reset_angle=True):
        if reset_angle:
            self.angle = [pi / 4, pi / 4, 0]
        return super().from_string(patternstring)

    def export_to_png(self, filename, *args, **kwargs):
        # Save parameters
        saved_parameters = (self.angle[:], self.size_hint[:], self.width, self.height)
        # Apply screen shot angle and size
        self.angle = [pi / 4, pi / 4, 0]
        self.size_hint = [None, None]
        self.width = min(self.size)
        self.height = min(self.size)
        # Update cube after changements
        self.update_cube()
        # take screenshot
        r = super().export_to_png(filename, *args, **kwargs)
        # Undo changements and update cube
        self.angle, self.size_hint, self.width, self.height = saved_parameters
        self.update_cube()
        return r


if __name__ == "__main__":
    from kivy.app import App

    class CubeApp(App):
        def build(self):
            return RubiksCube()

    CubeApp().run()
