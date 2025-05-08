from components.rubiks_cube_solver import RubiksCubeMaster
from time import sleep


def main():
    rcm = RubiksCubeMaster()
    print("RCM Init")
    sleep(1)
    rcm.m2.init()
    print("m2 init")
    rcm.solving = True
    rcm.flip_cube(5)


if __name__ == "__main__":
    main()
