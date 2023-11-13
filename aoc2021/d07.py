# coding: utf-8
from timeit import default_timer as timer

import numpy as np

# Main function
##########


def boom_part1(input_val, DBG=True):
    ia = np.asarray(input_val[0].split(","), dtype=int)
    cheapest_fuel = min(np.sum(np.abs(ia - pos)) for pos in ia)
    return cheapest_fuel


def boom_part2(input_val, DBG=True):
    ia = np.asarray(input_val[0].split(","), dtype=int)
    cheapest_fuel = np.inf
    for pos in range(np.min(ia), np.max(ia) + 1):
        distances = np.abs(ia - pos)
        cost_of_moving = np.sum(d * (d + 1) // 2 for d in distances)
        cheapest_fuel = min(cheapest_fuel, cost_of_moving)
    return cheapest_fuel


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


# Test cases
##########


tt1 = "16,1,2,0,4,2,7,1,2,14"
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 37, True)
test_part2(tt1, 168, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d07.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK =
# PART 2 OK =
