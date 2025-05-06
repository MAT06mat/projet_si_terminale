from components.rubiks_cube_solver import RubiksCubeMaster
from time import time


def main():
    rcm = RubiksCubeMaster()
    print("RCM Init")
    time(2)
    rcm.m1.init()
    print("m1 init")
    time(2)
    rcm.m2.init()
    print("m2 init")
