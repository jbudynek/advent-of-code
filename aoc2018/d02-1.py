# coding: utf-8

import time
from collections import Counter

import numpy as np


def function(ii, DBG=True):
    if DBG:
        print(ii)
    ret = [0, 0]
    cc = Counter(ii)
    for tt in cc:
        if cc[tt] == 3:
            ret[1] = 1
        elif cc[tt] == 2:
            ret[0] = 1
    if DBG:
        print(ret)
    return ret


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


t1 = "abcdef"
test(t1, [0, 0], True)  #

t2 = "bababc"
test(t2, [1, 1], True)  #

t3 = "abbcde"
test(t3, [1, 0], True)  #

t4 = "abcccd"
test(t4, [0, 1], True)  #

t5 = "aabcdd"
test(t5, [1, 0], True)  #

t6 = "abcdee"
test(t6, [1, 0], True)  #

t7 = "ababab"
test(t7, [0, 1], True)  #


INPUT_FILE = "input-d02.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
twos_and_threes = [0, 0]
for pp in puzzle_input:
    result = function(pp, False)
    twos_and_threes = np.add(twos_and_threes, result)
    kk = kk + 1
    # if (kk==10):break
print(twos_and_threes)
print(twos_and_threes[0] * twos_and_threes[1])

#################
