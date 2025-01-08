from PIL import Image
import colorsys


class Colors:
    WHITE = 0
    YELLOW = 1
    RED = 2
    ORANGE = 3
    BLUE = 4
    GREEN = 5

    def get_name(color):
        for key in Colors.__dict__:
            if Colors.__dict__[key] == color:
                return key


def get_color(img: Image.Image, x: int, y: int, size=20) -> str:
    r, g, b, tot = 0, 0, 0, 0

    for i in range(x - size, x + size):
        for j in (y - size, y + size):
            pixel = img.getpixel((i, j))
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
            tot += 1

    for i in range(-size, size):
        img.putpixel((x + i + 1, y - size), (255, 200, 100))
        img.putpixel((x + i, y + size), (255, 200, 100))
        img.putpixel((x - size, y + i), (255, 200, 100))
        img.putpixel((x + size, y + i + 1), (255, 200, 100))

    r /= tot
    g /= tot
    b /= tot

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


img: Image.Image = Image.open("python/image-viewer/img.png")

color = get_color(img, 400, 250)
name = Colors.get_color_name(color)
print(name)

# img.show()
