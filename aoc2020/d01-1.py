# coding: utf-8
import time

import numpy as np


def boom(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=np.int)
    if DBG:
        print(ii)
    len_ii = len(ii)
    for i in range(len_ii - 1):
        for j in range(i + 1, len_ii):
            if ii[i] + ii[j] == 2020:
                return ii[i] * ii[j]
    return -1


def boom2(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=np.int)
    product = [i * j for i in ii for j in ii if i > j and (i + j == 2020)]
    if DBG:
        print(product)
    return product[0]


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


t1 = """1721
979
366
299
675
1456"""
tt1 = t1.splitlines()
test(tt1, 514579, True)
# sys.exit()

INPUT_FILE = "input-d01.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# nested loops
ret = boom(puzzle_input, False)
print(ret)

# list comprenhension
ret = boom2(puzzle_input, False)
print(ret)

# part 1 = 1013211
