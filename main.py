import random
from copy import deepcopy

COLORS = [
    "\x1b[38;2;255;128;0m▄\x1b[0m",  # Orange
    "\x1b[38;2;0;255;0m▄\x1b[0m",  # Green
    "\x1b[38;2;255;255;255m▄\x1b[0m",  # White
    "\x1b[38;2;0;0;255m▄\x1b[0m",  # Blue
    "\x1b[38;2;255;255;0m▄\x1b[0m",  # Yellow
    "\x1b[38;2;255;0;0m▄\x1b[0m",  # Red
]


class Face:
    def __init__(self, color: int):
        self.color = color
        self.blocks = [color for i in range(8)]

    def turn(self, number=1):
        for i in range(number):
            self.blocks = self.blocks[6:] + self.blocks[:6]

    def get_side(self, side_index) -> list:
        self.turn(side_index - 1)
        new_side = self.blocks[:3]
        self.turn(5 - side_index)
        return new_side

    def set_side(self, side, new_side):
        self.turn(side - 1)
        self.blocks = new_side + self.blocks[3:8]
        self.turn(5 - side)

    @property
    def is_solved(self):
        return all([block == self.color for block in self.blocks])


class Cube:
    def __init__(self):
        self.faces = [Face(i) for i in range(6)]

    @property
    def is_solved(self):
        return all([face.is_solved for face in self.faces])

    def copy(self):
        return deepcopy(self)

    def random(self, number: int = None):
        if not number:
            number = random.randint(20, 30)
        for i in range(number):
            move = random.choice(["U", "D", "F", "B", "R", "L"])
            move = random.choice(["{move}", "2{move}", "{move}'"]).format(move=move)
            self.turn(move)

    def display(self):
        img = [[" " for i in range(15)] for i in range(11)]
        pos_list = ((4, 0), (0, 4), (4, 4), (8, 4), (12, 4), (4, 8))
        for i in range(6):
            x, y = pos_list[i]
            pixel_pos_list = (
                (x, y),
                (x + 1, y),
                (x + 2, y),
                (x + 2, y + 1),
                (x + 2, y + 2),
                (x + 1, y + 2),
                (x, y + 2),
                (x, y + 1),
            )
            for z in range(len(pixel_pos_list)):
                img[pixel_pos_list[z][1]][pixel_pos_list[z][0]] = COLORS[
                    self.faces[i].blocks[z]
                ]
            img[y + 1][x + 1] = COLORS[self.faces[i].color]

        print()
        for y in range(len(img)):
            for x in range(len(img[0])):
                print(img[y][x], end=" ")
                if x + 1 == len(img[0]):
                    print()
        print()

    def __rotate(self, faces_index: list[int], pos: list[int]):
        """1: UP .... 2: LEFT .... 3: DOWN .... 4: RIGHT"""

        faces = [self.faces[i] for i in faces_index]
        sides = [faces[i].get_side(pos[i]) for i in range(4)]
        for i in range(len(sides)):
            faces[i].set_side(pos[i], sides[i - 1])

    def turn(self, move: str):
        """NOTATIONS : https://jperm.net/3x3/moves"""

        if move[0] == "2":
            self.turn(move[-1])
            self.turn(move[-1])
            return
        elif move[-1] == "'":
            self.turn("2" + move[0])
            self.turn(move[0])
            return

        match move:
            case "U":
                self.faces[2].turn()
                self.__rotate((0, 3, 5, 1), (3, 2, 1, 4))
            case "D":
                self.faces[4].turn()
                self.__rotate((0, 1, 5, 3), (1, 2, 3, 4))
            case "F":
                self.faces[5].turn()
                self.__rotate((2, 3, 4, 1), (3, 3, 3, 3))
            case "B":
                self.faces[0].turn()
                self.__rotate((4, 3, 2, 1), (1, 1, 1, 1))
            case "R":
                self.faces[3].turn()
                self.__rotate((0, 4, 5, 2), (4, 2, 4, 4))
            case "L":
                self.faces[1].turn()
                self.__rotate((0, 2, 5, 4), (2, 2, 2, 4))


cube = Cube()
