# coding: utf-8

from collections import defaultdict

import numpy as np
from boilerplate import read_input_file, run_func


def binary(arr, target):
    count_dict = defaultdict(int)
    count = 0
    l_arr = len(arr)
    for i in range(2**l_arr):
        b = bin(i)[2:].zfill(l_arr)
        tot = 0
        for jdx in range(l_arr):
            if b[jdx] == "1":
                tot += arr[jdx]
                if tot > target:
                    break
        if tot == target:
            count += 1
            count_dict[b.count("1")] += 1

    return count, count_dict


def boom_part1(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=int)

    count, _ = binary(ii, 150)

    return count


def boom_part2(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=int)

    _, count_dict = binary(ii, 150)

    return count_dict[min(count_dict.keys())]


# Test cases
#############


t1 = """20
15
10
5
5"""
tt1 = t1.splitlines()
# test_func(boom_part1, tt1, 4, True) # returns 4 for target of 25, 0 for target of 150
# test_func(boom_part2, tt1, 3, True) # returns 3 for target of 25, 0 for target of 150

# Real data
############

puzzle_input = read_input_file("input-d17.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 4372
# PART 2 OK = 4
