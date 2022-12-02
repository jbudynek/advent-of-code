# coding: utf-8
from boilerplate import *


def get_cals_by_elf(input_val):
    input_val.append("")

    all_cals = []
    cur_cal = 0

    for line in input_val:
        if line == "":
            all_cals.append(cur_cal)
            cur_cal = 0
        else:
            cur_cal += int(line)
    sorted_cals = sorted(all_cals, reverse=True)
    return sorted_cals


def boom_part1(input_val, DBG=True):
    s_cals = get_cals_by_elf(input_val)
    return s_cals[0]


def boom_part2(input_val, DBG=True):
    s_cals = get_cals_by_elf(input_val)
    return sum(s_cals[0:3])

puzzle_input = read_input_file("input-d01.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 71506
# PART 2 OK = 209603
