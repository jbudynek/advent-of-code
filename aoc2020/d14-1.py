# coding: utf-8
import re
import time

import numpy as np


def boom(input_val, DBG=True):
    # mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    # mem[8] = 11

    mask = []
    mem = {}
    for instr in input_val:
        if "mask" in instr:
            mask = instr.split(" ")[2]
        else:
            nn = np.asarray(re.findall(r"\d+", instr), dtype=np.int)
            address = nn[0]
            val = nn[1]
            val_b = list("{0:036b}".format(val))
            if DBG:
                print("IN ", mask, address, "".join(val_b), val)
            for i in range(len(mask)):
                if mask[-1 - i] != "X":
                    val_b[-1 - i] = mask[-1 - i]
            val_b = "".join(val_b)
            val = int(val_b, 2)
            if DBG:
                print("OUT", mask, address, val_b, val)
            mem[address] = val

    return sum(mem.values())


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


t1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
tt1 = t1.splitlines()
test(tt1, 165, True)
# sys.exit()

INPUT_FILE = "input-d14.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 13105044880745
