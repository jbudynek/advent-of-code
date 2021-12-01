# coding: utf-8
from timeit import default_timer as timer

import numpy as np

# MAIN FUNCTION


def boom(input_val, DBG=True):
    depth = np.asarray(input_val, dtype=int)
    depth = np.append(depth, [np.NaN, np.NaN, np.NaN])
    depth_sum_window_3 = np.add(
        np.add(depth, np.roll(depth, 1)), np.roll(depth, 2))
    depth_sw3_roll_1 = np.roll(depth_sum_window_3, 1)
    delta = np.subtract(depth_sum_window_3, depth_sw3_roll_1)
    ret = np.sum(delta > 0)
    return ret

#############
#############
#############


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


##########
##########
##########

INPUT_FILE = "input-d01.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# OK 1362
