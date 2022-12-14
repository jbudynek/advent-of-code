# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func


def make_world(input_val):
    field = {}
    max_y = 0
    for line in input_val:
        ii = list(map(int, re.findall(r"-?\d+", line)))
        idx = 0
        while idx + 4 <= len(ii):
            (x0, y0) = (ii[idx + 0], ii[idx + 1])
            (x1, y1) = (ii[idx + 2], ii[idx + 3])
            max_y = max(max_y, y0, y1)
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    field[(x0, y)] = "#"
            elif y0 == y1:
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    field[(x, y0)] = "#"
            idx += 2
    return field, max_y


def update_field(field, cur_x, cur_y, dx, dy):
    del field[(cur_x, cur_y)]
    (cur_x, cur_y) = (cur_x + dx, cur_y + dy)
    field[(cur_x, cur_y)] = "#"
    return (cur_x, cur_y)


def fall_new_grain(field, max_y):
    (cur_x, cur_y) = (500, 0)
    field[(cur_x, cur_y)] = "#"

    while cur_y <= max_y:
        if not (cur_x, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 0, 1)
        elif not (cur_x - 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, -1, 1)
        elif not (cur_x + 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 1, 1)
        else:
            return True
    # grain falls out
    del field[(cur_x, cur_y)]
    return False


def fall_new_grain2(field, max_y):
    (cur_x, cur_y) = (500, 0)
    field[(cur_x, cur_y)] = "#"

    while cur_y <= max_y:  # I got lucky: this works
        if not (cur_x, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 0, 1)
        elif not (cur_x - 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, -1, 1)
        elif not (cur_x + 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 1, 1)
        else:
            # when cur_y==0, return False --> stop
            return cur_y > 0

    # grain of sand never falls out
    return True


def boom_part1(input_val, DBG=True):
    field, max_y = make_world(input_val)
    step = 0

    while True:
        grain_stays_in = fall_new_grain(field, max_y)
        if not grain_stays_in:
            break
        step += 1

    return step


def boom_part2(input_val, DBG=True):
    field, max_y = make_world(input_val)
    nb_grains = 0

    while True:
        grain_falls = fall_new_grain2(field, max_y)
        nb_grains += 1
        if not grain_falls:
            break

    return nb_grains


# Test cases
##########


t1 = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 24, True)
test_func(boom_part2, tt1, 93, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d14.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 913
# PART 2 OK = 30762
