# coding: utf-8

from io import StringIO

import numpy as np
from boilerplate import read_input_file, run_func, test_func


def parse_patterns(ipt):
    patterns = []
    cur_pattern = ""
    i = 0
    while i < len(ipt):
        line = ipt[i]
        if line == "":
            c = StringIO(cur_pattern)
            patterns.append(np.loadtxt(c, dtype=int))
            cur_pattern = ""

        line = line.replace("#", "1 ")
        line = line.replace(".", "0 ")
        cur_pattern += line + "\n"
        i += 1
    c = StringIO(cur_pattern)
    patterns.append(np.loadtxt(c, dtype=int))
    return patterns


def find_symmetry(pattern):
    num_y, num_x = pattern.shape
    id_x, id_y = 0, 0
    idxs = []
    idys = []
    for x in range(1, num_x):
        h_flip = True
        for y in range(num_y):
            _ll = pattern[y, :x]
            _rr = pattern[y, x:]
            sz = min(len(_ll), len(_rr))
            __ll = _ll[-sz:]
            __rr = _rr[:sz]
            if not np.array_equal(__ll, np.flip(__rr)):
                h_flip = False
                break
        if h_flip:
            id_x = x
            idxs.append(id_x)

    for y in range(1, num_y):
        v_flip = True
        for x in range(num_x):
            _uu = pattern[:y, x]
            _dd = pattern[y:, x]
            sz = min(len(_uu), len(_dd))
            __uu = _uu[-sz:]
            __dd = _dd[:sz]
            if not np.array_equal(__uu, np.flip(__dd)):
                v_flip = False
                break
        if v_flip:
            id_y = y
            idys.append(id_y)

    return idxs, idys


def find_other_symmetry(pattern, id_xs, id_ys):

    num_y, num_x = pattern.shape

    for x in range(num_x):
        for y in range(num_y):
            pattern2 = np.copy(pattern)
            pattern2[y, x] = 1 - pattern[y, x]
            nid_xs, nid_ys = find_symmetry(pattern2)
            if (len(nid_xs), len(nid_ys)) != (0, 0):
                nid_x = 0
                nid_y = 0
                for xx in nid_xs:
                    if xx not in id_xs:
                        nid_x = xx
                        break
                for yy in nid_ys:
                    if yy not in id_ys:
                        nid_y = yy
                        break
                if (nid_x, nid_y) != (0, 0):
                    return nid_x, nid_y


def boom_part1(ipt, DBG=True):
    ret = 0
    patterns = parse_patterns(ipt)
    for pattern in patterns:
        id_xs, id_ys = find_symmetry(pattern)
        if len(id_xs) > 1 or len(id_ys) > 1:
            print(id_xs, id_ys)
        id_x, id_y = 0, 0
        if len(id_xs) > 0:
            id_x = id_xs[0]
        if len(id_ys) > 0:
            id_y = id_ys[0]
        ret += id_x + (100 * id_y)
    return ret


def boom_part2(ipt, DBG=True):
    ret = 0
    patterns = parse_patterns(ipt)
    for pattern in patterns:
        id_xs, id_ys = find_symmetry(pattern)
        nid_x, nid_y = find_other_symmetry(pattern, id_xs, id_ys)
        ret += nid_x + (100 * nid_y)
    return ret


# Test cases
#############

ipt_test1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""".splitlines()
test_func(boom_part1, ipt_test1, 5, True)
test_func(boom_part2, ipt_test1, 300, True)

ipt_test1 = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()
test_func(boom_part1, ipt_test1, 400, True)
test_func(boom_part2, ipt_test1, 100, True)


ipt_test1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()
test_func(boom_part1, ipt_test1, 405, True)
test_func(boom_part2, ipt_test1, 400, True)

ipt_test1 = """.#.##.#.##..###
...##...#######
#.####.#.#.###.
#..##..##..#...
###..###....###
.##..##..#.#...
.#....#..######
#..##..########
########.#..#..""".splitlines()
test_func(boom_part2, ipt_test1, 14, True)

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 37381
# Part 2 solution: 28210
