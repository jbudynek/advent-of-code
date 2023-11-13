# coding: utf-8
import re
import time


def function(ii, DBG=True):

    # It contains a pair of any two letters that appears at least twice
    # in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa),
    # but not like aaa (aa, but it overlaps).

    # It contains at least one letter which repeats with exactly one letter
    # between them, like xyx, abcdefeghi (efe), or even aaa.

    # 2 letters repeated
    re2 = r"([a-z][a-z]).*\1"
    re22 = re.compile(re2)
    if re22.search(ii) is None:
        if DBG:
            print("pair")
        return False

    # 2 letters repeated
    re2 = r"([a-z]).\1"
    re22 = re.compile(re2)
    if re22.search(ii) is None:
        if DBG:
            print("rep")
        return False

    return True


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


t1 = "qjhvhtzxzqqjkmpb"
test(t1, True, False)  #

t2 = "xxyxx"
test(t2, True, False)  #

t3 = "uurcxstgmygtbstg"
test(t3, False, True)  #

t4 = "ieodomkazucvgmuy"
test(t4, False, True)  #

INPUT_FILE = "input-d05.txt"

f = open(INPUT_FILE, "r")
puzzle_input = [line.rstrip("\n") for line in f]
f.close()


nn = 0
for pp in puzzle_input:
    # print("*" + str(pp) + "**")
    result = function(pp, False)
    if result:
        nn = nn + 1
print(nn)

#################
