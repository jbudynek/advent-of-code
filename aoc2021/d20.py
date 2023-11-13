# coding: utf-8
from collections import Counter
from timeit import default_timer as timer

import numpy as np

# Helpers
##########


def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0] - 1
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1] - 1
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    # v_id = 0
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == "#":
                field[(x, y)] = 1
            else:
                field[(x, y)] = 0

    if DBG:
        print(field)

    return field


def get_bounds(tracks, DBG):
    coords = tracks.keys()
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]
    return (x_min, x_max, y_min, y_max)


# Main function
##########


def parse_algo(line):
    algo = np.zeros(512, dtype=int)
    idx = 0
    for cc in line:
        if cc == "#":
            algo[idx] = 1
        idx += 1
    return algo


def process(world, xy, algo, fill):
    dirs = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (0, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    bin_string = ""
    for d in dirs:
        nxy = (xy[0] + d[0], xy[1] + d[1])
        if nxy not in world:
            bin_string += str(fill)
        elif world[nxy] == 1:
            bin_string += "1"
        else:
            bin_string += "0"
    return int(bin_string, 2)


def enhance(input_val, nb_steps, DBG=True):
    algo = parse_algo(input_val[0])

    world = create_world(input_val[2:], DBG)

    if DBG:
        print_field(world)

    for step in range(nb_steps):

        fill = 0
        if algo[0] == 1:
            fill = step % 2

        (x_min, x_max, y_min, y_max) = get_bounds(world, DBG)

        new_world = world.copy()

        for x in range(x_min - 1, x_max + 2):
            for y in range(y_min - 1, y_max + 2):
                xy = (x, y)
                nxy_val = process(world, xy, algo, fill)
                new_world[xy] = algo[nxy_val]
        if DBG:
            print_field(new_world)
        world = new_world

    return Counter(new_world.values())[1]


def boom_part1(input_val, DBG=True):
    return enhance(input_val, 2, DBG)


def boom_part2(input_val, DBG=True):
    return enhance(input_val, 50, DBG)


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


# Test cases
##########


tt1 = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 35, True)
test_part2(tt1, 3351, False)

# Real data
##########

INPUT_FILE = "input-d20.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 5663
# PART 2 OK = 19638
