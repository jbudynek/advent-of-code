# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
# from collections import deque
import copy
import operator
import re
import string
import sys
import time
from enum import Enum
from timeit import default_timer as timer

import numpy as np


def next_value(value, subject_number):
    value = value * subject_number
    value = value % 20201227
    return value


def find_loop_size(pk, DBG):

    nb_loop = 0
    value = 1
    subject_number = 7

    while(True):
        nb_loop = nb_loop + 1
        value = next_value(value, subject_number)
        if value == pk:
            break

    return nb_loop


def apply_loop_size(pk, loop_size, DBG):

    value = 1
    for _ in range(loop_size):
        value = next_value(value, pk)

    return value

################


def boom(input_val, DBG=True):
    card_pk = int(input_val[0])
    door_pk = int(input_val[1])

    loop_size_card = find_loop_size(card_pk, DBG)
    loop_size_door = find_loop_size(door_pk, DBG)

    handshake_card = apply_loop_size(card_pk, loop_size_door, DBG)
    print("handshake_card", handshake_card)

    handshake_door = apply_loop_size(door_pk, loop_size_card, DBG)
    print("handshake_door", handshake_door)

    return handshake_card

########################


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
#######


print(find_loop_size(5764801, True))  # 8
print(find_loop_size(17807724, True))  # 11

#######

# card
# door

t1 = """5764801
17807724"""

tt1 = t1.splitlines()
test(tt1, 14897079, True)
# sys.exit()

#########

INPUT_FILE = "input-d25.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 2 = 4135
