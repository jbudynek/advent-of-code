# coding: utf-8
import re

import numpy as np
from boilerplate import read_input_file, run_func, test_func
from sympy import solve, symbols

# part 1: find intersections using cartesian equations of lines
# part 2: build a system of 6 equations with 6 unknowns, and let sympy solve it


def parse_stones(ipt):
    stones_pos = []
    stones_vel = []
    for line in ipt:
        ii = list(map(int, re.findall(r"-?\d+", line)))
        (x, y, z) = ii[0:3]
        (dx, dy, dz) = ii[3:6]
        stones_pos.append((x, y, z))
        stones_vel.append((dx, dy, dz))

    return stones_pos, stones_vel


def intersect_in_future_2d(stones_pos, stones_vel, i, j, DBG):
    (x1, y1, _) = stones_pos[i]
    (dx1, dy1, _) = stones_vel[i]
    (x2, y2, _) = stones_pos[j]
    (dx2, dy2, _) = stones_vel[j]

    # compute determinant to see if the lines are parallel
    if (dx1 * dy2 - dy1 * dx2) == 0:
        if DBG:
            print("parallel")
        return False, (None, None)  # parallel

    # for a line that passes by point = (x0,y0)
    # with direction = (u, v)
    # the cartesian equation is = x/u - y/v  = x0/u - y0/v
    # or a*x + b*y = d

    # line 1
    a1 = 1 / dx1
    b1 = -1 / dy1
    d1 = x1 / dx1 - y1 / dy1

    # line 2
    a2 = 1 / dx2
    b2 = -1 / dy2
    d2 = x2 / dx2 - y2 / dy2

    # we solve for the intersection using numpy
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([d1, d2])
    X = np.linalg.solve(A, B)

    (x, y) = (X[0], X[1])

    # then we compute scalar product between direction vector and
    # (origin, intersection), we want it positive to make sure the intersection
    # is in the "future"
    dxx1 = x - x1
    dyy1 = y - y1

    dxx2 = x - x2
    dyy2 = y - y2

    if DBG:
        print(
            i, j, "//", x1, y1, "-", dx1, dy1, "//", x2, y2, "-", dx2, dy2, "//", x, y
        )

    if (
        dx1 * dxx1 + dy1 * dyy1 > 0 and dx2 * dxx2 + dy2 * dyy2 > 0
    ):  # intersects in future
        return True, (x, y)

    if DBG:
        print("intersects in the past")
    return False, (None, None)  # intersects in past


def boom_part1(ipt, DBG=True):
    stones_pos, stones_vel = parse_stones(ipt)

    mi = 7 if DBG else 200_000_000_000_000
    ma = 27 if DBG else 400_000_000_000_000

    nb_stones = len(stones_pos)
    ans = 0
    for i in range(nb_stones):
        for j in range(i + 1, nb_stones):
            b, (x, y) = intersect_in_future_2d(stones_pos, stones_vel, i, j, DBG)
            if b and x >= mi and x <= ma and y >= mi and y <= ma:
                ans += 1
    return ans


def boom_part2(ipt, DBG=True):
    stones_pos, stones_vel = parse_stones(ipt)

    # for this part we have six unknowns: initial position and velocity of
    # the rock we throw - (x0,y0,z0) and (dx0,dy0,dz0)
    # to solve for six unknowns, we need a system of six equations/
    # we can pick any line in the input and get two equations, by saying
    # this line intersects the rock we throw:
    # rock line: x=x0+t*dx0, y=y0+t*dy0, z=z0+t*dz0
    # line1:     x=x1+t*dx1, y=y1+t*dy1, z=z1+t*dz1
    # intersection means there is a t where x, y, z are the same
    # for the two lines, e.g:
    # (x0-x1)/(dx0-dx1) = (y0-y1)/(dy0-dy1) = (z0-z1)/(dz0-dz1)
    # from this we get two equations:
    # (x0-x1)*(dy0-dy1)-(y0-y1)*(dx0-dx1) = 0
    # (y0-y1)*(dz0-dz1)-(z0-z1)*(dy0-dy1) = 0
    # let's do it for 3 arbitrary lines, that gives us 6 equations,
    # and let's hope the input data is well
    # formed and constrains the system enough.

    # the line made by the rock
    x0 = symbols("x")
    y0 = symbols("y")
    z0 = symbols("z")
    dx0 = symbols("dx")
    dy0 = symbols("dy")
    dz0 = symbols("dz")

    # three arbitrary lines from the input
    x1, y1, z1 = stones_pos[0]
    x2, y2, z2 = stones_pos[1]
    x3, y3, z3 = stones_pos[2]

    dx1, dy1, dz1 = stones_vel[0]
    dx2, dy2, dz2 = stones_vel[1]
    dx3, dy3, dz3 = stones_vel[2]

    # the equation system, let's use sympy to solve it.
    solutions = solve(
        [
            (x0 - x1) * (dy0 - dy1) - (y0 - y1) * (dx0 - dx1),
            (y0 - y1) * (dz0 - dz1) - (z0 - z1) * (dy0 - dy1),
            (x0 - x2) * (dy0 - dy2) - (y0 - y2) * (dx0 - dx2),
            (y0 - y2) * (dz0 - dz2) - (z0 - z2) * (dy0 - dy2),
            (x0 - x3) * (dy0 - dy3) - (y0 - y3) * (dx0 - dx3),
            (y0 - y3) * (dz0 - dz3) - (z0 - z3) * (dy0 - dy3),
        ],
        [x0, y0, z0, dx0, dy0, dz0],
        dict=True,
    )

    # for some reason we have several solutions, take one with integer values

    if DBG:
        print(solutions)
    for s in solutions:
        if s[dx0] == int(s[dx0]) and s[dy0] == int(s[dy0]) and s[dz0] == int(s[dz0]):
            return s[x0] + s[y0] + s[z0]


# Test cases
#############


ipt_test1 = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".splitlines()
test_func(boom_part1, ipt_test1, 2, True)
test_func(boom_part2, ipt_test1, 47, True)
# Real data
############

ipt_puzzle = read_input_file("input-d24.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 29142
# Part 2 solution: 848947587263033
