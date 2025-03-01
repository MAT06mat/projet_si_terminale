def test_cube():
    from imports import solver as s

    s.test(100)
    c = s.Cube()


def test_image_analyser():
    from imports import analyser as a

    img = a.Image.open("mods/analyser/img.png")
    anayser = a.FaceAnalyser(img, x=400, y=230, shape=120, squares=20)
    print(anayser.analyse())
    anayser.show()


def test_bluetooth():
    from imports import bluetooth_socket as bs
    from time import sleep

    server = bs.Server()
    server.connect()

    for i in range(3):
        print(i)
        sleep(10)

    server.deconnect()


def test_camera():
    from server.camera import Camera

    camera = Camera()
    img = camera.get_image()


if __name__ == "__main__":
    # test_cube()
    # test_image_analyser()
    test_bluetooth()
    pass
