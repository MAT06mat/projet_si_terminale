from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import colorsys


class FaceAnalyser:
    WHITE = "U"
    RED = "R"
    GREEN = "F"
    YELLOW = "D"
    ORANGE = "L"
    BLUE = "B"

    def __init__(self, x: int, y: int, shape: int, squares: int):
        self.img = None
        self.x = x
        self.y = y
        self.shape = shape
        self.squares = squares

    def average_color(self, x: int, y: int) -> tuple[float]:
        r, g, b, tot = 0, 0, 0, 0

        for i in range(x - self.squares, x + self.squares):
            for j in (y - self.squares, y + self.squares):
                if i % 4 == 1:
                    continue
                pixel = self.img.getpixel((i, j))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
                tot += 1

        for i in range(-self.squares, self.squares):
            self.img.putpixel((x + i + 1, y - self.squares), (255, 200, 100))
            self.img.putpixel((x + i, y + self.squares), (255, 200, 100))
            self.img.putpixel((x - self.squares, y + i), (255, 200, 100))
            self.img.putpixel((x + self.squares, y + i + 1), (255, 200, 100))

        r /= tot
        g /= tot
        b /= tot

        return r, g, b

    def sort_color(self, r, g, b) -> str:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

        # print(f"rgb({color[0]}, {color[1]}, {color[2]})")
        # print(f"hsv({h*360}, {s}, {v})")

        if s < 0.2:
            return self.WHITE
        elif h < 0.04:
            return self.RED
        elif h < 0.139:
            return self.ORANGE
        elif h < 0.194:
            return self.YELLOW
        elif h < 0.456:
            return self.GREEN
        elif h < 0.8:
            return self.BLUE
        else:
            return self.RED

    def face_order(self, face: str):
        f = face[0:3]
        f += face[5]
        f += face[6:9][::-1]
        f += face[3]
        f = {face[4]: f}
        return f

    def analyse(self, img: Image.Image):
        self.img = img
        face = ""
        for j in range(-1, 2):
            for i in range(-1, 2):
                rbg = self.average_color(
                    self.x + i * self.shape, self.y + j * self.shape
                )
                face += self.sort_color(*rbg)
        return self.face_order(face)

    def show(self):
        img = np.asarray(self.img)
        fig = plt.figure()
        fig.set_figwidth(12)
        fig.set_figheight(8)
        plt.imshow(img)
        plt.show()
