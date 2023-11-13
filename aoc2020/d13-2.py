# coding: utf-8
import time
from functools import reduce

import numpy as np

# The hardest part of this puzzle is to figure out that it can be solved using
# the Chinese remainder theorem.
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem

# En français : théorème des restes chinois
# https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_restes_chinois

# I used the implementation from RosettaCode
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def boom(input_val, DBG=True):

    # build the list of buses, and the list of expected deltas between them
    # dummy = int(input_val[0])
    buses = input_val[1].replace("x", "0").split(",")
    if DBG:
        print(buses)
    buses = np.asarray(buses, dtype=np.int64)
    nb_buses = len(buses)

    lhs_id = 0
    rhs_id = 1

    b = np.array(list(), dtype=np.int64)
    d = np.array(list(), dtype=np.int64)

    b = np.append(b, buses[lhs_id])

    while rhs_id < nb_buses:
        while buses[rhs_id] == 0:
            rhs_id = rhs_id + 1
        delta = rhs_id - lhs_id
        d = np.append(d, delta)
        b = np.append(b, buses[rhs_id])
        lhs_id = rhs_id
        rhs_id = lhs_id + 1

    if DBG:
        print(b, d)

    # prepare call to chinese remainder - need to cumsum the deltas
    # timestamp equals (sum of deltas form 0 to i) modulo (bus #i frequeny)
    n = b
    a = -np.cumsum(np.insert(d, 0, 0))

    if DBG:
        print(n, a)

    ret = chinese_remainder(n, a)

    return ret


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


t1 = """939
7,13,x,x,59,x,31,19"""
tt1 = t1.splitlines()
test(tt1, 1068781, True)
# sys.exit()

t1 = """939
17,x,13,19"""
tt1 = t1.splitlines()
test(tt1, 3417, True)
# sys.exit()

t1 = """939
67,7,59,61"""
tt1 = t1.splitlines()
test(tt1, 754018, False)
# sys.exit()

t1 = """939
67,x,7,59,61"""
tt1 = t1.splitlines()
test(tt1, 779210, False)
# sys.exit()

t1 = """939
67,7,x,59,61"""
tt1 = t1.splitlines()
test(tt1, 1261476, False)
# sys.exit()

t1 = """939
1789,37,47,1889"""
tt1 = t1.splitlines()
test(tt1, 1202161486, False)
# sys.exit()

INPUT_FILE = "input-d13.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 672754131923874
