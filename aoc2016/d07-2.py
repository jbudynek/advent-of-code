# coding: utf-8

import time

import numpy as np


def function(ii, DBG=True):

    if DBG:
        print("full address " + ii)

    # 1 find all ABAs, inside and outside
    # in intersection is not enmpty return True
    # else return false

    abas = {}
    abas[True] = []
    abas[False] = []
    lii = len(ii)

    in_brackets = False
    if (ii[0] == "[") or (ii[1] == "[") or (ii[2] == "["):
        in_brackets = True
    kk = 3
    while kk < lii + 1:

        test_aba = ii[kk - 3 : kk]  # noqa

        if DBG:
            print(str(kk) + " " + str(in_brackets) + " " + test_aba + " ")

        if (test_aba[0] == test_aba[2]) and (test_aba[0] != test_aba[1]):
            if in_brackets:
                abas[in_brackets].append(test_aba)
            else:
                abas[in_brackets].append(test_aba[1] + test_aba[0] + test_aba[1])

        if kk < lii:
            if ii[kk] == "[":
                in_brackets = True
            if ii[kk] == "]":
                in_brackets = False
        kk = kk + 1

    if DBG:
        print(abas)

    intersection = np.intersect1d(abas[True], abas[False])
    if DBG:
        print(intersection)

    return len(intersection) > 0


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


t1 = "aba[bab]xyz"
test(t1, True, True)  #

t2 = "xyx[xyx]xyx"
test(t2, False, True)  #

t3 = "aaa[kek]eke"
test(t3, True, True)  #

t4 = "zazbz[bzb]cdb"
test(t4, True, True)  #

INPUT_FILE = "input-d07.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
for pp in puzzle_input:
    result = function(pp, False)
    if result:
        nn = nn + 1
    kk = kk + 1
    # if (kk==10):break
print(nn)

#################
