# coding: utf-8
from timeit import default_timer as timer

import numpy as np


def get_mcb(candidates, k):
    nb_0 = 0
    nb_1 = 1
    for ll in candidates:
        if ll[k] == "0":
            nb_0 += 1
        if ll[k] == "1":
            nb_1 += 1
    if nb_0 < nb_1:
        return "1"
    else:
        return "0"


def filter_candidates(candidates, start_mcb):

    ret = []
    for ii in candidates:
        if ii.startswith(start_mcb):
            ret.append(ii)
    return ret


def boom(input_val, DBG=True):

    leng = len(input_val[0])

    # OXYGEN

    candidates = np.copy(input_val)

    start_mcb = ""

    for k in range(leng):

        mcb = get_mcb(candidates, k)
        start_mcb += str(mcb)
        candidates = filter_candidates(candidates, start_mcb)

        if len(candidates) == 1:
            break

    oxygen = candidates[0]

    # CARBON DIOXYDE

    candidates = np.copy(input_val)

    start_mcb = ""

    for k in range(leng):

        mcb = get_mcb(candidates, k)
        if mcb == "0":
            mcb = "1"
        else:
            mcb = "0"
        start_mcb += str(mcb)
        candidates = filter_candidates(candidates, start_mcb)

        if len(candidates) == 1:
            break

    carbon_dioxyde = candidates[0]

    return int(oxygen, 2) * int(carbon_dioxyde, 2)


#############


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

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


# TEST CASES

t1 = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
tt1 = t1.splitlines()
test(tt1, 230, True)
# sys.exit()

#############

INPUT_FILE = "input-d03.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# PART 2 - 4406844 OK
