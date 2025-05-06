from components.rubiks_cube_solver import RubiksCubeMaster


def test(func):
    def wrapper(*args, **kwargs):
        print(f"TEST: {func.__name__}")
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("-> Fail :", e)
        else:
            print("-> Sucess")
        finally:
            print("\n")

    return wrapper


@test
def test_cube():
    from imports import solver as s

    s.test(100)
    c = s.Cube()


@test
def test_image_analyser(rcm: RubiksCubeMaster):
    from imports import analyser as a

    img = a.Image.open("mods/analyser/img.png")
    print(rcm.anayser.analyse(img))
    # rcm.anayser.show()


@test
def test_bluetooth():
    from imports import bluetooth_socket as bs
    from time import sleep

    server = bs.Server()
    server.connect()

    for i in range(3):
        print(i)
        sleep(1)

    server.deconnect()


@test
def test_camera(rcm: RubiksCubeMaster):
    img = rcm.camera.get_image()


@test
def test_motors(rcm: RubiksCubeMaster):
    from time import sleep

    rcm.m1.init()
    sleep(1)
    for i in range(8):
        rcm.m1.turn()
        sleep(1)


if __name__ == "__main__":
    rcm = RubiksCubeMaster()
    test_cube()
    test_image_analyser(rcm)
    test_bluetooth()
    test_camera(rcm)
    test_motors(rcm)
