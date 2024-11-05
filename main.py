import random

COLORS = [
    "\x1b[38;2;255;128;0m▄\x1b[0m",  # Orange
    "\x1b[38;2;0;255;0m▄\x1b[0m",  # Green
    "\x1b[38;2;255;255;255m▄\x1b[0m",  # White
    "\x1b[38;2;0;0;255m▄\x1b[0m",  # Blue
    "\x1b[38;2;255;255;0m▄\x1b[0m",  # Yellow
    "\x1b[38;2;255;0;0m▄\x1b[0m",  # Red
]


class Cube:
    def __init__(self, values: list = None):
        self.orange = []
        self.green = []
        self.white = []
        self.blue = []
        self.yellow = []
        self.red = []
        self.faces = [
            self.orange,
            self.green,
            self.white,
            self.blue,
            self.yellow,
            self.red,
        ]
        if not values:
            values = [i for i in range(6)] * 8
            values.sort()

        for face in range(len(self.faces)):
            for i in range(8):
                self.faces[face].append(values[face * 8 + i])

    def random(self, number: int = None):
        if not number:
            number = random.randint(50, 200)
        for i in range(number):
            next_turn = random.choice(["U", "D", "F", "B", "R", "L"])
            self.turn(next_turn)

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
                    self.faces[i][z]
                ]
            img[y + 1][x + 1] = COLORS[i]

        print()
        for y in range(len(img)):
            for x in range(len(img[0])):
                print(img[y][x], end=" ")
                if x + 1 == len(img[0]):
                    print()
        print()

    def __change(self, list, new_list):
        list.clear()
        list.extend(new_list)

    def __shift(self, face, number=1):
        for i in range(number):
            self.__change(face, face[6:] + face[:6])

    def __get_side(self, face, side) -> list:
        self.__shift(face, side - 1)
        new_side = face[:3]
        self.__shift(face, 5 - side)
        return new_side

    def __set_side(self, face, side, new_side):
        self.__shift(face, side - 1)
        self.__change(face, new_side + face[3:8])
        self.__shift(face, 5 - side)

    def __rotate(self, faces_index: list[int], pos: list[int]):
        """1: UP .... 2: LEFT .... 3: DOWN .... 4: RIGHT"""

        faces = [self.faces[i] for i in faces_index]
        sides = [self.__get_side(faces[i], pos[i]) for i in range(4)]
        for i in range(len(sides)):
            self.__set_side(faces[i], pos[i], sides[i - 1])

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
                self.__shift(self.white)
                self.__rotate((0, 3, 5, 1), (3, 2, 1, 4))
            case "D":
                self.__shift(self.yellow)
                self.__rotate((0, 1, 5, 3), (1, 2, 3, 4))
            case "F":
                self.__shift(self.red)
                self.__rotate((2, 3, 4, 1), (3, 3, 3, 3))
            case "B":
                self.__shift(self.orange)
                self.__rotate((4, 3, 2, 1), (1, 1, 1, 1))
            case "R":
                self.__shift(self.blue)
                self.__rotate((0, 4, 5, 2), (4, 2, 4, 4))
            case "L":
                self.__shift(self.green)
                self.__rotate((0, 2, 5, 4), (2, 2, 2, 4))


cube = Cube()
# cube.random()

text = ""
while text.lower() != "exit":
    cube.display()
    text = input("Next turn : ")
    cube.turn(text.upper())
