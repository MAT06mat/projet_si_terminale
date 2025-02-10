from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Mesh
import numpy as np
from math import cos, sin

from imports import solver


CN = solver.CubeNotation
FACE_ORDER = solver.FACE_ORDER


class Cubie(Widget):
    def __init__(self, parent, r_pos: list[int]):
        self.parent = parent
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

    def is_face_visible(self, face: str) -> bool:
        """
        Check if the specified face is visible.
        """
        reversed = 1
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

    def project_point(
        self, point: list, r_pos: list, rotation: list, mult: int, angle=[0, 0, 0]
    ):
        """
        Project a 3D point to 2D.
        """
        r = rotation
        if angle != [0, 0, 0]:
            internal_rotation = self.get_rotation_matrix(angle)
            r = rotation * internal_rotation

        offset_point = point + r_pos
        rotated2d = np.dot(r, offset_point.reshape((3, 1)))

        # Project the 3D points to 2D
        projected2d = np.dot(self.projection_matrix, rotated2d)

        x = int(projected2d[0, 0] * mult) + self.parent.center_x
        y = int(projected2d[1, 0] * mult) + self.parent.center_y

        return np.array([x, y])

    def render(self, rotation: list, mult: int, angle=[0, 0, 0]) -> None:
        """
        Render the cubie.
        """
        # Update projected points
        for i, point in enumerate(self.points):
            self.projected_points[i] = self.project_point(
                point, self.r_pos, rotation, mult, angle
            )

        # Draw the faces of the cube
        for face in self.faces_to_render:
            Color(*self.faces_color[face])
            self.draw_face(face)
