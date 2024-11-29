import random, kociemba


SOLVED_CUBE_STRING = "UUUUUUUURRRRRRRRFFFFFFFFDDDDDDDDLLLLLLLLBBBBBBBB"
FACE_ORDER = "URFDLB"


class __Cube__:
    def __init__(self, cube_string=SOLVED_CUBE_STRING) -> None:
        self.cube_string: str = cube_string

    def is_solve(self) -> bool:
        return self.cube_string == SOLVED_CUBE_STRING

    def to_kociemba(self) -> str:
        faces = []
        for i in range(0, len(self.cube_string), 8):
            faces.append(self.cube_string[i : i + 8])
        f = ""
        for i, face in enumerate(faces):
            f += face[0:3]
            f += face[7]
            f += FACE_ORDER[i]
            f += face[3]
            f += face[6]
            f += face[5]
            f += face[4]
        return f

    def get_face(self, face: str) -> str:
        index = FACE_ORDER.index(face)
        return self.cube_string[index * 8 : (index + 1) * 8]

    def get_side(self, face: str, side: str) -> str:
        face = self.get_face(face)
        match side:
            case "U":
                return face[:3]
            case "R":
                return face[2:5]
            case "D":
                return face[4:7]
            case "L":
                return face[6:8] + face[0]

    def set_side(self, face: str, side: str, pos: str) -> None:
        i = FACE_ORDER.index(face) * 8
        match pos:
            case "U":
                self.cube_string = (
                    self.cube_string[:i] + side + self.cube_string[i + 3 :]
                )
            case "R":
                self.cube_string = (
                    self.cube_string[: i + 2] + side + self.cube_string[i + 5 :]
                )
            case "D":
                self.cube_string = (
                    self.cube_string[: i + 4] + side + self.cube_string[i + 7 :]
                )
            case "L":
                self.cube_string = (
                    self.cube_string[:i]
                    + side[2]
                    + self.cube_string[i + 1 : i + 6]
                    + side[:2]
                    + self.cube_string[i + 8 :]
                )

    def f_rotate(self, face: str) -> None:
        index = FACE_ORDER.index(face) * 8
        self.cube_string = (
            self.cube_string[:index]
            + self.cube_string[index + 6 : index + 8]
            + self.cube_string[index : index + 6]
            + self.cube_string[index + 8 :]
        )

    def random(self, nb: int) -> None:
        for i in range(nb):
            f = FACE_ORDER[random.randint(0, 5)]
            n = random.randint(1, 3)
            self.turn(str(f) + str(n))

    def turn(self, move: str) -> None:
        if len(move) == 1:
            f = move
            nb = "1"
        else:
            f, nb = move
        if nb != "1":
            if nb == "2":
                self.turn(f + "1")
            else:
                self.turn(f + "2")
        table = {
            "U": ("BRFL", "UUUU"),
            "R": ("BDFU", "LRRR"),
            "F": ("URDL", "DLUR"),
            "D": ("BLFR", "DDDD"),
            "L": ("BUFD", "RLLL"),
            "B": ("DRUL", "DRUL"),
        }[f]
        self.f_rotate(f)
        sides = [self.get_side(table[0][i], table[1][i]) for i in range(4)]
        for i, f in enumerate(table[0]):
            self.set_side(f, sides[i - 1], table[1][i])


class Cube:
    def __init__(self, patternstring: str | None = None) -> None:
        """Initialize the cube"""
        self.__cube__ = __Cube__()
        if patternstring:
            self.from_string(patternstring)

    def from_string(self, patternstring: str) -> bool:
        """Construct a cube from a string."""
        if len(patternstring) < 48:
            print(
                "Error: Cube definition string "
                + patternstring
                + " contains less than 48 facelets."
            )
            return False
        elif len(patternstring) > 48:
            print(
                "Error: Cube definition string "
                + patternstring
                + " contains more than 48 facelets."
            )
            return False
        for i in FACE_ORDER:
            if patternstring.count(i) != 8:
                print(
                    "Error: Cube definition string "
                    + patternstring
                    + " does not contain exactly 8 facelets of each color."
                )
                return False
        try:
            kociemba.solve(__Cube__(patternstring).to_kociemba())
        except ValueError as e:
            print(e)
            return False
        self.__cube__.cube_string = patternstring
        return True

    def to_string(self, kociemba=False) -> str:
        """Return the string of the cube"""
        if kociemba:
            return self.__cube__.to_kociemba()
        else:
            return self.__cube__.cube_string

    def is_solve(self) -> bool:
        """Return if True the cube is solve"""
        return self.__cube__.is_solve()

    def solve(self, patternstring: str | None = None, max_depth: int = 24) -> str:
        """Solve a cube and return the solution"""
        if self.__cube__.is_solve():
            return "Already solve"
        return kociemba.solve(self.__cube__.to_kociemba(), patternstring, max_depth)

    def random(self, nb: int = random.randint(20, 30)) -> None:
        """Randomize the cube"""
        self.__cube__.random(nb)
