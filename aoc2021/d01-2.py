# coding: utf-8
import numpy as np

#############


def boom(input_val, DBG=True):
    depth = np.asarray(input_val, dtype=int)
    depth = np.append(depth, [np.NaN, np.NaN, np.NaN])
    depth_sum_window_3 = np.add(
        np.add(depth, np.roll(depth, 1)), np.roll(depth, 2))
    depth_sw3_roll_1 = np.roll(depth_sum_window_3, 1)
    delta = np.subtract(depth_sum_window_3, depth_sw3_roll_1)
    ret = np.sum(delta > 0)
    return ret

#############


##########

INPUT_FILE = "input-d01.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)

print(ret)

# OK 1362
