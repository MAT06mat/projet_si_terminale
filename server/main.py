"""from solver import Cube, test
from analyser import FaceAnalyser, Image

test(100)
c = Cube()

print()

img = Image.open("server/analyser/img.png")
anayser = FaceAnalyser(img, x=400, y=230, shape=120, squares=20)
print(anayser.analyse())
anayser.show()"""

from imports import bluetooth_socket as bs


if __name__ == "__main__":
    from time import sleep

    server = bs.Server()
    server.connect()

    for i in range(4):
        print(i)
        sleep(10)

    server.deconnect()
