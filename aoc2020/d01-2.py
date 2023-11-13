# coding: utf-8
import random
import time
from timeit import default_timer as timer

import numpy as np


def boom(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=np.int)
    if DBG:
        print(ii)
    len_ii = len(ii)
    for i in range(len_ii - 2):
        for j in range(i + 1, len_ii - 1):
            for k in range(j + 1, len_ii):
                if DBG:
                    print(ii[i] + ii[j] + ii[k])
                if ii[i] + ii[j] + ii[k] == 2020:
                    return ii[i] * ii[j] * ii[k]
    return -1


# list comprehension is more elegant but slower
def boom2(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=np.int)
    if DBG:
        print(ii)
    product = [
        i * j * k
        for i in ii
        for j in ii
        for k in ii
        if i > j and j > k and (i + j + k == 2020)
    ]
    if DBG:
        print(product)
    return product[0]


# generator is more elegant but slower
def boom3(input_val, DBG=True):
    ii = np.asarray(input_val, dtype=np.int)
    if DBG:
        print(ii)
    product = next(
        i * j * k
        for i in ii
        for j in ii
        for k in ii
        if i > j and j > k and (i + j + k == 2020)
    )
    if DBG:
        print(product)
    return product


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
test(tt1, 241861950, True)
# sys.exit()

INPUT_FILE = "input-d01.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# nested loops
times = []
for n in range(20):
    random.shuffle(puzzle_input)
    start = timer()
    ret = boom(puzzle_input, False)
    end = timer()
    times.append(end - start)
print("loops", sum(times) / len(times), ret)

# list comprehension
times = []
for n in range(20):
    random.shuffle(puzzle_input)
    start = timer()
    ret = boom2(puzzle_input, False)
    end = timer()
    times.append(end - start)
print("comp", sum(times) / len(times), ret)

# generator
times = []
for n in range(20):
    random.shuffle(puzzle_input)
    start = timer()
    ret = boom3(puzzle_input, False)
    end = timer()
    times.append(end - start)
print("gen", sum(times) / len(times), ret)

# part 2 = 13891280
