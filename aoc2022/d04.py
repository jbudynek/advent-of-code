# coding: utf-8
import re

import numpy as np
from boilerplate import read_input_file, run_func, test_func


def parse_line(line):
    rr = np.asarray(re.split(r"-|,", line), dtype=int)
    ar0 = np.arange(rr[0], rr[1] + 1)
    ar1 = np.arange(rr[2], rr[3] + 1)
    return ar0, ar1


def overlaps_totally(line):
    ar0, ar1 = parse_line(line)
    intersect = np.intersect1d(ar0, ar1)
    return np.array_equal(ar0, intersect) or np.array_equal(ar1, intersect)


def overlaps_partially(line):
    ar0, ar1 = parse_line(line)
    return len(np.intersect1d(ar0, ar1)) > 0


def boom_part1(input_val, DBG=True):
    over = [overlaps_totally(line) for line in input_val]
    return sum(over)


def boom_part2(input_val, DBG=True):
    over = [overlaps_partially(line) for line in input_val]
    return sum(over)


# Test cases
##########


tt1 = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
tt1 = tt1.splitlines()  # type: ignore
test_func(boom_part1, tt1, 2, True)
test_func(boom_part2, tt1, 4, True)

# Real data
##########

puzzle_input = read_input_file("input-d04.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 567
# PART 2 OK = 907
