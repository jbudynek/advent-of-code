# coding: utf-8

from collections import deque

import numpy as np
from boilerplate import read_input_file, run_func, test_func


def predict_left_right(ts):
    dq = deque()
    cur_ts = ts
    while True:
        dq.append(cur_ts)
        dd = np.ediff1d(cur_ts)
        cur_ts = dd
        if sum(np.abs(dd)) == 0:
            ans_left, ans_right = 0, 0
            while dq:
                ts = dq.pop()
                ans_right += ts[-1]
                ans_left = -ans_left + ts[0]
            return ans_left, ans_right


def boom_part1(ipt, DBG=True):

    return sum([predict_left_right([int(x) for x in line.split()])[1] for line in ipt])


def boom_part2(ipt, DBG=True):

    return sum([predict_left_right([int(x) for x in line.split()])[0] for line in ipt])


# Test cases
#############


ipt_test1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()
test_func(boom_part1, ipt_test1, 114, True)
test_func(boom_part2, ipt_test1, 2, True)

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

# Part 1 solution: 1479011877
# Part 2 solution: 973
