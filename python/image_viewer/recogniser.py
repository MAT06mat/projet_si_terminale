from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import colorsys


SHAPE_SIZE = 120
SQUARES_SIZE = 20
ANALYSER_POS = (400, 230)

X = ANALYSER_POS[0]
Y = ANALYSER_POS[1]


class Colors:
    WHITE = 0
    YELLOW = 1
    RED = 2
    ORANGE = 3
    BLUE = 4
    GREEN = 5

    def to_name(color: int | list | tuple) -> list | str:
        if type(color) in (list, tuple):
            return list(map(Colors.to_name, color))
        for key in Colors.__dict__:
            if Colors.__dict__[key] == color:
                return key


class Anayser:
    def average_color(self, x: int, y: int) -> tuple[float]:
        r, g, b, tot = 0, 0, 0, 0

        for i in range(x - SQUARES_SIZE, x + SQUARES_SIZE):
            for j in (y - SQUARES_SIZE, y + SQUARES_SIZE):
                pixel = self.img.getpixel((i, j))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
                tot += 1

        for i in range(-SQUARES_SIZE, SQUARES_SIZE):
            self.img.putpixel((x + i + 1, y - SQUARES_SIZE), (255, 200, 100))
            self.img.putpixel((x + i, y + SQUARES_SIZE), (255, 200, 100))
            self.img.putpixel((x - SQUARES_SIZE, y + i), (255, 200, 100))
            self.img.putpixel((x + SQUARES_SIZE, y + i + 1), (255, 200, 100))

        r /= tot
        g /= tot
        b /= tot

        return r, g, b

    def sort_color(self, r, g, b) -> str:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

        # print(f"rgb({color[0]}, {color[1]}, {color[2]})")
        # print(f"hsv({h*360}, {s}, {v})")

        if s < 0.2:
            return Colors.WHITE
        elif h < 0.04:
            return Colors.RED
        elif h < 0.139:
            return Colors.ORANGE
        elif h < 0.194:
            return Colors.YELLOW
        elif h < 0.456:
            return Colors.GREEN
        elif h < 0.8:
            return Colors.BLUE
        else:
            return Colors.RED

    def face_detection(self):
        colors = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                rbg = self.average_color(X + i * SHAPE_SIZE, Y + j * SHAPE_SIZE)
                name = self.sort_color(*rbg)
                colors.append(name)
        return colors

    def show(self):
        img = np.asarray(self.img)
        fig = plt.figure()
        fig.set_figwidth(12)
        fig.set_figheight(8)
        plt.imshow(img)
        plt.show()

    def analyse(self, img: Image.Image, show=True):
        self.img = img

        colors = self.face_detection()
        names = Colors.to_name(colors)

        if show:
            self.show()

        return names


if __name__ == "__main__":
    img = Image.open("python/image_viewer/img.png")
    result = Anayser().analyse(img)
    print(result)
