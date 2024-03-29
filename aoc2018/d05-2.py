# coding: utf-8

import time

import numpy as np


def function(ii, DBG=True):
    delta = np.abs(ord("A") - ord("a"))

    minret = 100000

    for letter in range(0, 26):
        lc = chr(ord("a") + letter)
        uc = chr(ord("A") + letter)
        if DBG:
            print("***" + str(lc) + "***")
        idx = 0
        list_ii = np.array(list(ii))
        while idx < len(list_ii) - 1:
            if list_ii[idx] == lc or list_ii[idx] == uc:
                list_ii = np.delete(list_ii, idx)
                idx = max(0, idx - 2)
            elif np.abs(ord(list_ii[idx]) - ord(list_ii[idx + 1])) == delta:
                list_ii = np.delete(list_ii, idx)
                list_ii = np.delete(list_ii, idx)
                idx = max(0, idx - 2)
            else:
                idx = idx + 1
        if DBG:
            print("***" + "".join(list_ii) + "***")
        ret = len(list_ii)
        if DBG:
            print("***" + str(ret) + "***")
        if ret < minret:
            minret = ret
    return minret


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


t1 = "dabAcCaCBAcCcaDA"
test(t1, 4, True)  #

# sys.exit()

INPUT_FILE = "input-d05.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
f.close()
puzzle_input = contents.rstrip()

ret = function(puzzle_input, True)  #
print(ret)
