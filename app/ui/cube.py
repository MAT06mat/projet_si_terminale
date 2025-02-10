from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Mesh, Rectangle
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
from kivy.metrics import dp
import numpy as np
from math import cos, sin, pi

from imports import solver


CN = solver.CubeNotation
FACE_ORDER = solver.FACE_ORDER


class Cubie(Widget):
    def __init__(self, parent, r_pos: list[int]):
        self.parent: RubiksCube = parent
        self.r_pos = r_pos  # Relative position
        self.angle = [0, 0, 0]
        # Define the 8 points of the cube
        self.points = [
            np.matrix([-1, -1, 1]),
            np.matrix([1, -1, 1]),
            np.matrix([1, 1, 1]),
            np.matrix([-1, 1, 1]),
            np.matrix([-1, -1, -1]),
            np.matrix([1, -1, -1]),
            np.matrix([1, 1, -1]),
            np.matrix([-1, 1, -1]),
        ]
        # Define the projection matrix
        self.projection_matrix = np.matrix([[1, 0, 0], [0, 1, 0]])
        self.projected_points = [[n, n] for n in range(len(self.points))]

        self.faces_to_render = ""
        if r_pos[2] > 0:
            self.faces_to_render += CN.B
        elif r_pos[2] < 0:
            self.faces_to_render += CN.F
        if r_pos[1] < 0:
            self.faces_to_render += CN.D
        if r_pos[1] > 0:
            self.faces_to_render += CN.U
        if r_pos[0] > 0:
            self.faces_to_render += CN.L
        if r_pos[0] < 0:
            self.faces_to_render += CN.R
        self.update_colors()

    def get_points(self, face: str) -> list[list[int]]:
        """
        Get the points of the specified face.
        """
        p = self.projected_points
        match face:
            case CN.B:
                return [p[0], p[1], p[2], p[3]]
            case CN.F:
                return [p[4], p[5], p[6], p[7]]
            case CN.D:
                return [p[0], p[1], p[5], p[4]]
            case CN.U:
                return [p[2], p[3], p[7], p[6]]
            case CN.L:
                return [p[1], p[2], p[6], p[5]]
            case CN.R:
                return [p[0], p[3], p[7], p[4]]

    def get_rotation_matrix(self, angle):
        # Define the rotation matrices
        rotation_x = np.matrix(
            [
                [1, 0, 0],
                [0, cos(angle[0]), -sin(angle[0])],
                [0, sin(angle[0]), cos(angle[0])],
            ]
        )

        rotation_y = np.matrix(
            [
                [cos(angle[1]), 0, sin(angle[1])],
                [0, 1, 0],
                [-sin(angle[1]), 0, cos(angle[1])],
            ]
        )

        rotation_z = np.matrix(
            [
                [cos(angle[2]), -sin(angle[2]), 0],
                [sin(angle[2]), cos(angle[2]), 0],
                [0, 0, 1],
            ]
        )

        return rotation_x * rotation_y * rotation_z

    def is_face_visible(self, face: str, reversed: int = 1) -> bool:
        """
        Check if the specified face is visible.
        """
        if face in CN.B + CN.R:
            reversed = -1
        p1, p2, p3, _ = self.get_points(face)
        # Convert points to 3D NumPy arrays
        p1 = np.array([p1[0], p1[1], 0])
        p2 = np.array([p2[0], p2[1], 0])
        p3 = np.array([p3[0], p3[1], 0])
        # Calculate the normal vector of the face
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2) * reversed
        # The face is visible if the z component of the normal is negative
        return normal[2] < 0

    def update_colors(self):
        self.faces_color = {}
        for face in self.faces_to_render:
            match face:
                case CN.U:
                    r_pos = np.matrix((-self.r_pos[0], -self.r_pos[2]))
                case CN.D:
                    r_pos = np.matrix((-self.r_pos[0], self.r_pos[2]))
                case CN.R:
                    # Rotate r_pos 90 degrees for RL faces
                    rotation_matrix = np.matrix([[0, 1], [-1, 0]])
                    r_pos = np.dot(
                        rotation_matrix,
                        np.matrix((self.r_pos[1], self.r_pos[2])).T,
                    ).T
                case CN.L:
                    # Rotate r_pos 90 degrees for RL faces
                    rotation_matrix = np.matrix([[0, 1], [-1, 0]])
                    r_pos = np.dot(
                        rotation_matrix, np.matrix((self.r_pos[1], -self.r_pos[2])).T
                    ).T
                case CN.F:
                    # Rotate r_pos 180 degrees for FB faces
                    rotation_matrix = np.matrix([[-1, 0], [0, -1]])
                    r_pos = np.dot(
                        rotation_matrix, np.matrix((self.r_pos[0], self.r_pos[1])).T
                    ).T
                case CN.B:
                    # Rotate r_pos 180 degrees for FB faces
                    rotation_matrix = np.matrix([[-1, 0], [0, -1]])
                    r_pos = np.dot(
                        rotation_matrix, np.matrix((-self.r_pos[0], self.r_pos[1])).T
                    ).T
            r_pos //= 2
            x = r_pos[0, 0] + 1
            y = r_pos[0, 1] + 1
            cube_string = self.parent.to_string(True)
            face_index = FACE_ORDER.index(face)
            face_colors = cube_string[face_index * 9 : face_index * 9 + 9]
            color = face_colors[3 * y + x]
            color = self.parent.faces_colors[color]
            self.faces_color[face] = color

    def draw_face(self, face: str) -> None:
        """
        Draw the specified face.
        """
        if not self.is_face_visible(face):
            return
        Color(*self.faces_color[face])
        points = self.get_points(face)
        Mesh(
            vertices=[
                points[0][0],
                points[0][1],
                0,
                0,
                points[1][0],
                points[1][1],
                0,
                0,
                points[2][0],
                points[2][1],
                0,
                0,
                points[3][0],
                points[3][1],
                0,
                0,
            ],
            indices=[0, 1, 2, 2, 3, 0],
            mode="triangles",
        )
        Color(*self.parent.border_color)
        for i in range(4):
            Line(
                points=[
                    points[i][0],
                    points[i][1],
                    points[(i + 1) % 4][0],
                    points[(i + 1) % 4][1],
                ],
                width=self.parent.border,
                cap="round",
                joint="round",
            )

    def project_point(self, point: list, r_pos: list, rotation: list, mult: int):
        """
        Project a 3D point to 2D.
        """
        offset_point = point + r_pos
        r = rotation
        if self.angle != [0, 0, 0]:
            internal_rotation = self.get_rotation_matrix(self.angle)
            r = rotation * internal_rotation

        rotated2d = np.dot(r, offset_point.reshape((3, 1)))

        # Project the 3D points to 2D
        projected2d = np.dot(self.projection_matrix, rotated2d)

        x = int(projected2d[0, 0] * mult) + self.parent.center_x
        y = int(projected2d[1, 0] * mult) + self.parent.center_y

        return np.array([x, y])

    def render(self, rotation: list, mult: int) -> None:
        """
        Render the cubie.
        """
        # Update projected points
        for i, point in enumerate(self.points):
            self.projected_points[i] = self.project_point(
                point, self.r_pos, rotation, mult
            )

        # Draw the faces of the cube
        for face in self.faces_to_render:
            self.draw_face(face)


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
    Background color of the widget.
    """

    border_color = ColorProperty((0.1, 0.1, 0.1, 1))
    """
    Color of the border lines around each face.
    """

    frame_rate = NumericProperty(1 / 60)
    """
    Frame rate of updating cube.
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
    Color of each face.
    """

    _last_touch_pos = None
    """
    Last touch position for tracking touch movement.
    """

    _cube_string = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._cubies = [
            Cubie(self, r_pos=[2 * x, 2 * y, 2 * z])
            for x in range(-1, 2)
            for y in range(-1, 2)
            for z in range(-1, 2)
            if (x, y, z) != (0, 0, 0)
        ]
        self.bind(_cube_string=self.update_colors)
        Clock.schedule_interval(self.update_cube, self.frame_rate)

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
            ):
                self.turn(self._last_face_touch)
            Window.set_system_cursor("arrow")
            return True
        return super().on_touch_up(touch)

    def turn(self, move):
        face = move[0]
        for cubie in self._cubies:
            if face in cubie.faces_to_render:
                match face:
                    case CN.B:
                        cubie.angle[2] = pi / 2
                    case CN.F:
                        cubie.angle[2] = -pi / 2
                    case CN.U:
                        cubie.angle[1] = pi / 2
                    case CN.D:
                        cubie.angle[1] = -pi / 2
                    case CN.L:
                        cubie.angle[0] = pi / 2
                    case CN.R:
                        cubie.angle[0] = -pi / 2
                Animation(angle=[0, 0, 0], d=0.5, t="in_out_sine").start(cubie)
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

        rotation = self._cubies[0].get_rotation_matrix(self.angle)
        mult = self.get_mult()

        self.canvas.clear()
        with self.canvas:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)
            for cubie in self._cubies:
                if cubie.angle == [0, 0, 0]:
                    cubie.render(rotation, mult)
            # Render cubies with animation after other
            for cubie in self._cubies:
                if cubie.angle != [0, 0, 0]:
                    cubie.render(rotation, mult)


if __name__ == "__main__":
    from kivy.app import App

    class CubeApp(App):
        def build(self):
            return RubiksCube()

    CubeApp().run()
