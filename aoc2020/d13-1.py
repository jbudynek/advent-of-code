# coding: utf-8
import operator
import time

import numpy as np


def boom(input_val, DBG=True):

    earliest_tmst = int(input_val[0])
    buses = input_val[1].replace("x", "0").split(",")
    buses = np.asarray(buses, dtype=np.int)

    deltas = {}

    for bus_id in buses:
        if bus_id == 0:
            continue
        next_available_departure = earliest_tmst // bus_id * bus_id + bus_id
        deltas[bus_id] = next_available_departure - earliest_tmst
        if DBG:
            print(bus_id, next_available_departure, deltas[bus_id])

    my_bus = min(deltas.items(), key=operator.itemgetter(1))[0]
    if DBG:
        print(deltas, my_bus)
    return my_bus * deltas[my_bus]


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
test(tt1, 295, True)
# sys.exit()

INPUT_FILE = "input-d13.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 3269
