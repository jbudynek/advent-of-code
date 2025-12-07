import re
import numpy as np

ipt_test = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test


world = {}
max_y = len(ipt)
max_x = len(ipt[0])
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        world[(x, y)] = c

# we can do both parts at the same time.
# use dynamic programming for part 2
# and remember splits we see, in a set

SET_SPLITS = set()
CACHE = {}


def count_ways(y, x):
    if (y, x) in CACHE:
        return CACHE[(y, x)]
    if y == max_y:
        return 1

    while world[(x, y)] != "^":
        y += 1
        if y == max_y:
            return 1
    # count split for part 1
    SET_SPLITS.add((x, y))
    # count left and right
    lhs = count_ways(y + 1, x - 1)
    CACHE[(y + 1, x - 1)] = lhs
    rhs = count_ways(y + 1, x + 1)
    CACHE[(y + 1, x + 1)] = rhs
    ret = lhs + rhs
    CACHE[(y, x)] = ret
    return ret


res2 = count_ways(0, max_x // 2)
res1 = len(SET_SPLITS)


print(f"# Part 1 solution: {res1}")
print(f"# Part 2 solution: {res2}")

# Part 1 solution: 1672
# Part 2 solution: 231229866702355
