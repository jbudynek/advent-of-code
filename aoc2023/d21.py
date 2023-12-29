# coding: utf-8
import numpy as np
from boilerplate import read_input_file, run_func, test_func
from scipy.interpolate import lagrange


def print_field_complex(field, x_min, x_max, y_min, y_max):
    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if complex(xx, yy) in field:
                ss += str(field[complex(xx, yy)])
            else:
                ss += " "
        print(ss)


def parse_world(ccc, DBG=True):
    x_min, x_max, y_min, y_max = 0, len(ccc[0]), 0, len(ccc)
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == "#":
                field[complex(x, y)] = c
            elif c == "S":
                field[complex(x, y)] = c

    if DBG:
        print(field)
    return field, x_min, x_max, y_min, y_max


def count(field):
    plots = [1 if (z == "O" or z == "S") else 0 for z in field.values()]
    return sum(plots)


def step(field, x_max, y_max):
    dirs = [complex(0, 1) ** i for i in range(4)]
    field2 = field.copy()
    for k, v in field.items():
        if v == "O" or v == "S":
            for d in dirs:
                nk = k + d
                nkr_mod = (k.real + d.real) % x_max
                nki_mod = (k.imag + d.imag) % y_max
                nk_mod = nkr_mod + 1j * nki_mod
                if (nk_mod not in field or field[nk_mod] != "#") and nk not in field:
                    field2[nk] = "O"
            del field2[k]
    return field2


def boom_part1(ipt, DBG=True):
    field, x_min, x_max, y_min, y_max = parse_world(ipt, DBG)

    max_step = 6 if DBG else 64
    nb_step = 0

    if DBG:
        print("step", nb_step)
        print_field_complex(field, x_min, x_max, y_min, y_max)

    while True:
        if nb_step == max_step:
            return count(field)
        field = step(field, x_max, y_max)
        nb_step += 1
        if DBG:
            print("step", nb_step)
            print_field_complex(field, x_min, x_max, y_min, y_max)


def boom_part2(ipt, DBG=True):
    field, x_min, x_max, y_min, y_max = parse_world(ipt, DBG)

    max_step = x_max // 2 + 2 * x_max + 1
    nb_step = 0

    if DBG:
        print("step", nb_step)
        print_field_complex(field, x_min, x_max, y_min, y_max)

    xx = []
    yy = []
    while nb_step < max_step:
        field = step(field, x_max, y_max)
        nb_step += 1
        if nb_step in [x_max // 2, x_max // 2 + x_max, x_max // 2 + 2 * x_max]:
            if DBG:
                print("*step", nb_step, count(field))
            xx.append(nb_step)
            yy.append(count(field))
        if DBG and nb_step in [6, 10, 50]:
            print("step", nb_step, count(field))

    # the map is periodical in space, and there are straight paths from
    # the center to the borders. So the number of tiles should also be
    # interesting to look at when
    # n_steps is equal to x_max (131), modulo x_max//2 (65)
    # we are in 2D plane so we suspect a quadratic relationship
    # n = a*x^2 + b*x + c where n = nb_tiles, x = nb_steps
    # use Lagrange interpolation to fit a polynomial to three values
    # for steps = (x_max//2) (x_max//2 + x_max) (x_max//2 + 2 * x_max)
    # note 26501365 is also of this form (xmax//2 + N * xmax)
    # *step 65 3797
    # *step 196 34009
    # *step 327 94353

    poly = lagrange(xx, yy)

    return int(np.ceil(poly(26501365)))


# Test cases
#############


ipt_test1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()
test_func(boom_part1, ipt_test1, 16, True)
test_func(boom_part2, ipt_test1, 528192700299084, True)

# Real data
############

ipt_puzzle = read_input_file("input-d21.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 3716
# Part 2 solution: 616583483179597
