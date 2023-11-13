# coding: utf-8
import time
from collections import Counter


def comp(ii, jj, DBG=True):
    lii = len(ii)
    nbdiff = 0
    ret = ""
    for idx in range(lii):
        if ii[idx] != jj[idx]:
            nbdiff = nbdiff + 1
            if nbdiff > 1:
                return ""
        else:
            ret = ret + ii[idx]
    return ret


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


t1 = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""


def find_box_id(ids, DBG=True):
    nbids = len(ids)
    for idx in range(nbids):
        for jdx in range(idx + 1, nbids):
            ccomp = comp(ids[idx], ids[jdx])
            if ccomp != "":
                print(ccomp)
                break


find_box_id(t1.splitlines(), True)  #


INPUT_FILE = "input-d02.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

find_box_id(puzzle_input, True)  #


#################
