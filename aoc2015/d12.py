# coding: utf-8
import json
import re

import numpy as np
from boilerplate import read_input_file, run_func, test_func


# Main function
##########
def boom_part1(input_val, DBG=True):
    rr = re.findall(r"-?\d+", input_val[0])
    ii = np.asarray(rr, dtype=int)
    return np.sum(ii)


def has_red_val(obj):
    for v in obj.values():
        if v == "red":
            return True
    return False


def count_all(obj):
    total = 0
    if isinstance(obj, dict):
        if not has_red_val(obj):
            for k in obj.keys():
                total += count_all(obj[k])
    elif isinstance(obj, list):
        for k in obj:
            total += count_all(k)
    else:
        try:
            total += int(obj)
        except ValueError:
            pass
    return total


def boom_part2(input_val, DBG=True):
    total = 0
    json_object = json.loads(input_val[0])
    total += count_all(json_object)

    return total


# Test cases
##########

tt1 = '[1,{"c":"red","b":2},3]'
tt1 = tt1.splitlines()  # type: ignore
test_func(boom_part1, tt1, 6, True)
test_func(boom_part2, tt1, 4, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d12.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 111754
# PART 2 OK = 65402
