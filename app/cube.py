from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Mesh
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.input.motionevent import MotionEvent
from kivy.clock import Clock
from kivy.core.window import Window
import numpy as np
from math import cos, sin, pi

WHITE = (0.9, 0.9, 0.9)
BLACK = (0.1, 0.1, 0.1)


class FaceColors:
    U = (1, 1, 1)
    R = (0.72, 0.07, 0.20)
    F = (0, 0.61, 0.28)
    D = (1, 0.84, 0)
    L = (1, 0.35, 0)
    B = (0, 0.27, 0.68)


class RubiksColors:
    U = ((FaceColors.U for j in range(3)) for i in range(3))
    R = ((FaceColors.R for j in range(3)) for i in range(3))
    F = ((FaceColors.F for j in range(3)) for i in range(3))
    D = ((FaceColors.D for j in range(3)) for i in range(3))
    L = ((FaceColors.L for j in range(3)) for i in range(3))
    B = ((FaceColors.B for j in range(3)) for i in range(3))


class CubeWidget(Widget):
    angle = ListProperty([0, 0, 0])
    scale = NumericProperty(40)
    border = NumericProperty(3)
    rotate_on_x = BooleanProperty(True)
    rotate_on_y = BooleanProperty(True)
    relative_pos = ListProperty([0, 0, 0])
    last_mouse_pos = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

        # Schedule the update function to be called 60 times per second
        Clock.schedule_interval(self.update, 1 / 60)

    def on_touch_down(self, touch: MotionEvent):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.last_mouse_pos = touch.pos
            Window.set_system_cursor("hand")
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            dx = touch.pos[0] - self.last_mouse_pos[0]
            dy = touch.pos[1] - self.last_mouse_pos[1]

            if self.rotate_on_y:
                self.angle[0] -= dy * 0.01
            if self.rotate_on_x:
                s = 1
                if pi / 2 < self.angle[0] < 3 * pi / 2:
                    s = -1
                self.angle[1] += dx * 0.01 * s

            self.last_mouse_pos = touch.pos

            self.angle[0] %= 2 * pi
            self.angle[1] %= 2 * pi
            self.angle[2] %= 2 * pi

            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            Window.set_system_cursor("arrow")
            return True
        return super().on_touch_up(touch)

    def is_face_visible(self, p1, p2, p3, reversed=1):
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

    def draw_face(self, points, color, reversed=1):
        if self.is_face_visible(points[0], points[1], points[2], reversed):
            Color(*color)
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
            Color(*BLACK)
            for i in range(4):
                Line(
                    points=[
                        points[i][0],
                        points[i][1],
                        points[(i + 1) % 4][0],
                        points[(i + 1) % 4][1],
                    ],
                    width=self.border,
                    cap="round",
                    joint="round",
                )

    def update(self, *args):
        # Define the rotation matrices
        rotation_z = np.matrix(
            [
                [cos(self.angle[2]), -sin(self.angle[2]), 0],
                [sin(self.angle[2]), cos(self.angle[2]), 0],
                [0, 0, 1],
            ]
        )

        rotation_y = np.matrix(
            [
                [cos(self.angle[1]), 0, sin(self.angle[1])],
                [0, 1, 0],
                [-sin(self.angle[1]), 0, cos(self.angle[1])],
            ]
        )

        rotation_x = np.matrix(
            [
                [1, 0, 0],
                [0, cos(self.angle[0]), -sin(self.angle[0])],
                [0, sin(self.angle[0]), cos(self.angle[0])],
            ]
        )

        self.canvas.clear()
        with self.canvas:
            for i, point in enumerate(self.points):
                p = point + self.relative_pos

                # Apply the rotation matrices to the points
                rotated2d = np.dot(rotation_z, p.reshape((3, 1)))
                rotated2d = np.dot(rotation_y, rotated2d)
                rotated2d = np.dot(rotation_x, rotated2d)

                # Project the 3D points to 2D
                projected2d = np.dot(self.projection_matrix, rotated2d)

                if self.width > self.height:
                    size = self.height / 2
                else:
                    size = self.width / 2

                mult = self.scale / 100 * size

                x = int(projected2d[0, 0] * mult) + self.center_x
                y = int(projected2d[1, 0] * mult) + self.center_y

                self.projected_points[i] = np.array([x, y])

            p = self.projected_points
            # Draw the faces of the cube
            self.draw_face([p[0], p[1], p[2], p[3]], FaceColors.B, reversed=-1)
            self.draw_face([p[4], p[5], p[6], p[7]], FaceColors.F)
            self.draw_face([p[0], p[1], p[5], p[4]], FaceColors.D)
            self.draw_face([p[2], p[3], p[7], p[6]], FaceColors.U)
            self.draw_face([p[1], p[2], p[6], p[5]], FaceColors.L)
            self.draw_face([p[0], p[3], p[7], p[4]], FaceColors.R, reversed=-1)


class CubeApp(App):
    def build(self):
        Window.clearcolor = WHITE
        return CubeWidget()


if __name__ == "__main__":
    CubeApp().run()
