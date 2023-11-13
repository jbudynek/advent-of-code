# coding: utf-8
from timeit import default_timer as timer

import numpy as np

# Main function
##########


def boom_part1(input_val, DBG=True):
    # ugly way, by growing a list!
    ia = np.asarray(input_val[0].split(","), dtype=int)

    nb_z = 0
    for day in np.arange(1, 81):
        ia = ia - 1
        ia[ia == -1] = 6
        ia = np.append(ia, [8] * nb_z)
        nb_z = np.count_nonzero(ia == 0)
        if DBG:
            lenia = len(ia)
            print(day, lenia, ia)

    return len(ia)


def boom_part2(input_val, DBG=True):
    # ok way, by counting the right things and not worrying about the list.
    ia = np.asarray(input_val[0].split(","), dtype=int)

    status_to_count = np.zeros(9, dtype=int)

    for i in ia:
        status_to_count[i] += 1
    nb_z = 0
    for day in np.arange(1, 257):
        loopy = status_to_count[0]
        for i in range(1, 9):
            status_to_count[i - 1] = status_to_count[i]
        status_to_count[6] += loopy
        status_to_count[8] = nb_z
        nb_z = status_to_count[0]
        if DBG:
            print(day, status_to_count)

    return np.sum(status_to_count)


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


tt1 = "3,4,3,1,2"
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 5934, True)
test_part2(tt1, 26984457539, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d06.txt"
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

# PART 1 OK = 386536
# PART 2 OK = 1732821262171
