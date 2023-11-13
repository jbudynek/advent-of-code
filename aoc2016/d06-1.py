# coding: utf-8

import time
from collections import Counter


def function(ii, DBG=True):

    ll = len(ii[0])
    if DBG:
        print(ll)
    a = list()

    for k in range(ll):
        a.append(list())

    for i in ii:
        for k in range(ll):
            a[k].append(i[k : k + 1])  # noqa

    ret_most = ""
    ret_least = ""
    for k in range(ll):
        colk = "".join(a[k])
        ctrk = Counter(colk)
        if DBG:
            print(ctrk)
        rm = ctrk.most_common(1)[0][0]  # most common
        rl = ctrk.most_common()[-1][0]  # least common

        ret_most = ret_most + rm
        ret_least = ret_least + rl

    return (ret_most, ret_least)


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


t1 = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""
test(t1.splitlines(), ("easter", "advent"), True)  #


INPUT_FILE = "input-d06.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

result = function(puzzle_input, False)
print(result)
