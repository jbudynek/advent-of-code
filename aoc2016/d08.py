# coding: utf-8
import re

import numpy as np
from boilerplate import read_input_file, run_func, test_func

# Main function
################

H = 6
W = 50


def boom_part1(input_val, DBG=True):
    matrix = np.zeros((H, W), dtype=int)

    for line in input_val:
        numbers = list(map(int, re.findall(r"-?\d+", line)))
        if "rect" in line:
            a = 0
            b = numbers[1]
            c = 0
            d = numbers[0]
            matrix[a:b, c:d] = 1
        elif "row" in line:
            row_id = numbers[0]
            delta = numbers[1]
            row = matrix[row_id, :].copy()
            row = np.roll(row, delta)
            matrix[row_id, :] = row
        elif "column" in line:
            column_id = numbers[0]
            delta = numbers[1]
            column = matrix[:, column_id].copy()
            column = np.roll(column, delta)
            matrix[:, column_id] = column

        else:
            quit()

    for line in matrix:
        to_print = ""
        for val in line:
            if val == 1:
                to_print += "*"
            else:
                to_print += " "
        print(to_print)

    return np.sum(matrix)


def boom_part2(input_val, DBG=True):
    return -1


# Test cases
#############


t1 = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""
tt1 = t1.splitlines()
H = 3
W = 7
test_func(boom_part1, tt1, 6, True)

# Real data
############

puzzle_input = read_input_file("input-d08.txt")

# part 1
H = 6
W = 50

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

# r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")

quit()

# PART 1 OK = 116
# PART 2 OK = UPOJFLBCEZ
