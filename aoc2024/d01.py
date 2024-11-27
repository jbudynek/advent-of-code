# coding: utf-8
import numpy as np
from boilerplate import read_input_file, run_func, test_func


def strings_to_int_array(ii):
    ii = ii.split(",")
    ii = np.asarray(ii, dtype=int)
    return ii


def boom_part1(ipt, DBG=True):
    ia = strings_to_int_array(ipt[0])
    return np.sum(ia)


def boom_part2(ipt, DBG=True):
    return -1


# Test cases
#############


ipt_test1 = "3,4,3,1,2".splitlines()
test_func(boom_part1, ipt_test1, 13, True)
test_func(boom_part2, ipt_test1, -1, True)

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

# Part 1 solution:
# Part 2 solution:
