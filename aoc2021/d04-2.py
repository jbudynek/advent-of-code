# coding: utf-8
from timeit import default_timer as timer

import numpy as np

##########
# TODO Should all be redone with np matrix
##########


def parse_boards(input_val, DBG=True):
    k = 0
    ret = []
    while k < len(input_val):
        bb = []
        bb.append(np.asarray(input_val[k].split(), dtype=int))
        bb.append(np.asarray(input_val[k + 1].split(), dtype=int))
        bb.append(np.asarray(input_val[k + 2].split(), dtype=int))
        bb.append(np.asarray(input_val[k + 3].split(), dtype=int))
        bb.append(np.asarray(input_val[k + 4].split(), dtype=int))
        k = k + 6
        if DBG:
            print(bb)
        ret.append(bb)
        if DBG:
            print(k, len(input_val))
    if DBG:
        print("***", ret)
    return ret


def set_in_board(b, dd, DBG):
    for ll in b:
        for idx in range(5):
            if ll[idx] == dd:
                ll[idx] = -1
    return b


def board_line(b, DBG):
    for idx in range(5):
        if (
            b[idx][0] == -1
            and b[idx][1] == -1
            and b[idx][2] == -1
            and b[idx][3] == -1
            and b[idx][4] == -1
        ):
            return True
    for v in range(5):
        if (
            b[0][v] == -1
            and b[1][v] == -1
            and b[2][v] == -1
            and b[3][v] == -1
            and b[4][v] == -1
        ):
            return True
    return False


def board_remain(bb, DBG):
    ret = 0
    for ll in bb:
        for idx in range(len(ll)):
            if not ll[idx] == -1:
                ret += ll[idx]
    return ret


def boom(input_val, DBG=True):

    drawn = np.asarray(input_val[0].split(","), dtype=int)
    if DBG:
        print(drawn)

    del input_val[0]
    del input_val[0]

    if DBG:
        print(input_val)

    boards = parse_boards(input_val, DBG)
    if DBG:
        print("******", boards, "*******")

    for dd in drawn:
        idb = 0
        while idb < len(boards):
            bb = boards[idb]
            bb = set_in_board(bb, dd, DBG)
            if board_line(bb, DBG):
                if DBG:
                    print("***QUINE***", dd, bb, "QUINE", boards)
                del boards[idb]
                idb = idb - 1
                if len(boards) == 0:
                    return dd * board_remain(bb, DBG)
            idb += 1
        # if DBG:print(dd,boards)


# Testing and timing
##########


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


# Test cases
##########

tt1 = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

tt1 = tt1.splitlines()  # type: ignore
test(tt1, 1924, True)
# sys.exit()

##########

INPUT_FILE = "input-d04.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# PART 2 OK = 17408
