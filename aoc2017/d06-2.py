# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from collections import deque
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
import pickle
import copy
import operator
import re
import string
import sys
import time
from timeit import default_timer as timer

import numpy as np


def parse_input(input_val):
    ii = input_val.split("\t")
    ii = np.asarray(ii, dtype=int)
    return ii


def next_state(blocks):
    # find highest block
    # distribute
    argmax = np.argmax(blocks)
    val = blocks[argmax]
    l = len(blocks)
    new_blocks = blocks.copy()

    new_blocks[argmax] = 0
    idx = (argmax + 1) % l
    while (val > 0):
        new_blocks[idx] += 1
        val -= 1
        idx = (idx+1) % l

    return new_blocks


def loop(blocks, DBG=True):
    cache = set()
    blocks.flags.writeable = False
    cache.add(hash(blocks.data.tobytes()))

    round = 1

    while(True):
        new_blocks = next_state(blocks)
        if DBG:
            print(round, new_blocks)
        # check if in cache
        new_blocks.flags.writeable = False
        hnb = hash(new_blocks.data.tobytes())
        if hnb in cache:
            return (round, new_blocks)
        else:
            round += 1
            cache.add(hnb)
            blocks = new_blocks


def boom(input_val, DBG=True):
    blocks = parse_input(input_val)
    if DBG:
        print(blocks)

    (round, blocks) = loop(blocks, DBG)

    (round, blocks) = loop(blocks,DBG)

    return round

#############
############
#############


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


##########
################
# TEST CASES
#########
###########

tt1 = "0\t2\t7\t0"
test(tt1, 4, True)
# sys.exit()

INPUT_FILE = "input-d06.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input[0], DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# 1695 OK