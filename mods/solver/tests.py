from mods.solver.cube import PublicCube
from tqdm import tqdm
from time import time


def test(nb, moves=30):
    ttot, tmax, mtot, mmax = 0, 0, 0, 0
    mmin, tmin = 99, 99
    solves = []
    for i in tqdm(range(nb)):
        cube = PublicCube()
        cube.random(moves)

        t1 = time()
        sol = cube.solve()
        t2 = time()

        sol = sol.split(" ")
        for s in sol:
            cube._cube.turn(s)
        solves.append(cube.is_solve())

        t = t2 - t1
        ttot += t
        m = len(sol)
        mtot += m

        tmin = min(t, tmin)
        tmax = max(t, tmax)
        mmin = min(m, mmin)
        mmax = max(m, mmax)

    print("Time average :", ttot / nb)
    print("Moves average :", mtot / nb)
    print("Time min / max :", tmin, tmax)
    print("Moves min / max :", mmin, mmax)
    print("Solves :", solves.count(True), "/", len(solves))
