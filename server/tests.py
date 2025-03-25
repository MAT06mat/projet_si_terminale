def test_cube():
    from imports import solver as s

    s.test(100)
    c = s.Cube()


def test_image_analyser():
    from imports import analyser as a

    img = a.Image.open("mods/analyser/img.png")
    anayser = a.FaceAnalyser(x=400, y=230, shape=120, squares=20)
    print(anayser.analyse(img))
    # anayser.show()


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


def test_motors():
    from server.motors import Motors
    from time import sleep

    m = Motors().get_turn_motor(1)
    m.init()
    sleep(1)
    for i in range(8):
        m.turn()
        sleep(1)


def test(func):
    print(f"TEST: {func.__name__}")
    try:
        func()
    except Exception as e:
        print("-> Fail :", e)
    else:
        print("-> Sucess")
    finally:
        print("\n")


if __name__ == "__main__":
    test(test_cube)
    test(test_image_analyser)
    test(test_bluetooth)
    test(test_camera)
    test(test_motors)
