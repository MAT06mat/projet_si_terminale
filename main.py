import random, kociemba
from time import time
from tqdm import tqdm


COLORS = {
    "U": "\x1b[38;2;255;255;0m▄\x1b[0m",
    "R": "\x1b[38;2;0;255;0m▄\x1b[0m",
    "F": "\x1b[38;2;255;0;0m▄\x1b[0m",
    "D": "\x1b[38;2;255;255;255m▄\x1b[0m",
    "L": "\x1b[38;2;0;0;255m▄\x1b[0m",
    "B": "\x1b[38;2;255;128;0m▄\x1b[0m",
}


class Cube:
    def __init__(self):
        self.f = "UUUUUUUURRRRRRRRFFFFFFFFDDDDDDDDLLLLLLLLBBBBBBBB"
        self.faces_order = "URFDLB"

    def from_string(self, s: str):
        """Construct a facelet cube from a string."""
        if len(s) < 48:
            return (
                "Error: Cube definition string "
                + s
                + " contains less than 48 facelets."
            )
        elif len(s) > 48:
            return (
                "Error: Cube definition string "
                + s
                + " contains more than 48 facelets."
            )
        for i in self.faces_order:
            if s.count(i) != 8:
                return (
                    "Error: Cube definition string "
                    + s
                    + " does not contain exactly 8 facelets of each color."
                )
        self.f = s
        return True

    def to_kociemba(self) -> str:
        faces = []
        for i in range(0, len(self.f), 8):
            faces.append(self.f[i : i + 8])
        f = ""
        for i, face in enumerate(faces):
            f += face[0:3]
            f += face[7]
            f += self.faces_order[i]
            f += face[3]
            f += face[6]
            f += face[5]
            f += face[4]
        return f

    def solve(self, patternstring: str | None = None, max_depth: int = 24) -> str:
        if self.f == "UUUUUUUURRRRRRRRFFFFFFFFDDDDDDDDLLLLLLLLBBBBBBBB":
            return "Already solve"
        return kociemba.solve(self.to_kociemba(), patternstring, max_depth)

    def get_face(self, face):
        index = self.faces_order.index(face)
        return self.f[index * 8 : (index + 1) * 8]

    def get_side(self, face, side):
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

    def set_side(self, face, side, pos):
        i = self.faces_order.index(face) * 8
        match pos:
            case "U":
                self.f = self.f[:i] + side + self.f[i + 3 :]
            case "R":
                self.f = self.f[: i + 2] + side + self.f[i + 5 :]
            case "D":
                self.f = self.f[: i + 4] + side + self.f[i + 7 :]
            case "L":
                self.f = (
                    self.f[:i]
                    + side[2]
                    + self.f[i + 1 : i + 6]
                    + side[:2]
                    + self.f[i + 8 :]
                )

    def f_rotate(self, face):
        index = self.faces_order.index(face) * 8
        self.f = (
            self.f[:index]
            + self.f[index + 6 : index + 8]
            + self.f[index : index + 6]
            + self.f[index + 8 :]
        )

    def random(self, nb: int = None):
        if not nb:
            nb = random.randint(20, 30)
        for i in range(nb):
            f = self.faces_order[random.randint(0, 5)]
            n = random.randint(1, 3)
            self.turn(str(f) + str(n))

    def display(self):
        img = [[" " for i in range(15)] for i in range(11)]
        pos_list = ((4, 0), (8, 4), (4, 4), (4, 8), (0, 4), (12, 4))
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
            fc = self.faces_order[i]
            f = self.get_face(fc)
            for z in range(len(pixel_pos_list)):
                img[pixel_pos_list[z][1]][pixel_pos_list[z][0]] = COLORS[f[z]]
            img[y + 1][x + 1] = COLORS[fc]

        print()
        for y in range(len(img)):
            for x in range(len(img[0])):
                print(img[y][x], end=" ")
                if x + 1 == len(img[0]):
                    print()
        print()

    def turn(self, move):
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

    def test(nb, moves=30):
        ttot, tmax, mtot, mmax = 0, 0, 0, 0
        mmin, tmin = 99, 99
        solves = []
        for i in tqdm(range(nb)):
            cube = Cube()
            cube.random(moves)

            t1 = time()
            sol = cube.solve()
            t2 = time()

            sol = sol.split(" ")
            for s in sol:
                cube.turn(s)
            solves.append(cube.f == "UUUUUUUURRRRRRRRFFFFFFFFDDDDDDDDLLLLLLLLBBBBBBBB")

            t = t2 - t1
            ttot += t
            m = len(sol)
            mtot += m

            tmin = min(t, tmin)
            tmax = max(t, tmax)
            mmin = min(m, mmin)
            mmax = max(m, mmax)

        print("Time average :", ttot / nb)
        print("Moves average :", mtot / nb)
        print("Time max / min :", tmax, tmin)
        print("Moves max / min :", mmax, mmin)
        print("Solves :", solves.count(True), "/", len(solves))

    def control(self):
        self.display()
        while True:
            m = input("Next move: ").upper()
            if len(m) > 2:
                m = m[:2]
            if len(m) == 0:
                continue
            if len(m) == 1:
                m += "1"
            if m[1] not in "123" or m[0] not in self.faces_order:
                print(f"Error: {m} is not a valid move")
                continue
            self.turn(m)
            self.display()
