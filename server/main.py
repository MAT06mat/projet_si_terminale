def test_cube():
    from solver import Cube, test

    test(100)
    c = Cube()


def test_image_analyser():
    from analyser import FaceAnalyser, Image

    img = Image.open("server/analyser/img.png")
    anayser = FaceAnalyser(img, x=400, y=230, shape=120, squares=20)
    print(anayser.analyse())
    anayser.show()


def test_bluetooth():
    from imports import bluetooth_socket as bs
    from time import sleep

    server = bs.Server()
    server.connect()

    for i in range(4):
        print(i)
        sleep(5)

    server.deconnect()


if __name__ == "__main__":
    # test_cube()
    # test_image_analyser()
    # test_bluetooth()
    pass
