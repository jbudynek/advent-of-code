# coding: utf-8
import numpy as np

##########


def boom(input_val, DBG=True):
    depth = np.asarray(input_val, dtype=int)
    depth = np.append(depth, np.NaN)
    depth_2 = np.roll(depth, 1)
    delta = np.subtract(depth, depth_2)
    ret = np.sum(delta > 0)
    return ret


##########

INPUT_FILE = "input-d01.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)

print(ret)

# OK 1387
