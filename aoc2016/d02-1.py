# coding: utf-8

import sys
import time

keyboard = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
]


def min_max(nn, mini, maxi):
    if nn < mini:
        return mini
    elif nn > maxi:
        return maxi
    else:
        return nn


def function(ii, DBG=True):

    if DBG:
        print(ii)

    out = ""
    cur_x = 1
    cur_y = 1

    for iii in ii:

        for dir in iii:
            if dir == "U":
                cur_y = min_max((cur_y + 1), 0, 2)
            elif dir == "D":
                cur_y = min_max((cur_y - 1), 0, 2)
            elif dir == "L":
                cur_x = min_max((cur_x - 1), 0, 2)
            elif dir == "R":
                cur_x = min_max((cur_x + 1), 0, 2)
            else:
                print("***" + str(dir) + "***")
                sys.exit()
        out = out + str(keyboard[cur_y][cur_x])
    return out


def test(cc=None, expected=None, DBG=False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc, DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "*** " + str(cc) + " *** -> Result = " + str(result),
        " -> success = " + str(flag) + " -> expected " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


t1 = """ULL
RRDDD
LURDL
UUUUD"""
tt = t1.splitlines()

test(tt, 1985, True)  #

INPUT_FILE = "input-d02.txt"

f = open(INPUT_FILE, "r")
puzzle_input = [line.rstrip("\n") for line in f]
f.close()

result = test(puzzle_input, 0, False)
