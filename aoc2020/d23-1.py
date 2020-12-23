# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
import copy
import operator
import re
import string
import sys
import time
from collections import deque
from timeit import default_timer as timer

import numpy as np

# use a deque

def parse_cups(input_val, DBG):

    circle = deque()
    for ii in input_val:
        circle.append(int(ii))

    if DBG:
        print(circle)

    return circle


def play_round(circle, move_id, DBG):
    max_cup = 9

    if DBG:
        print("cups: ", circle)

    current_cup = circle[0]
    circle.rotate(-1)

    three_cups = [circle.popleft(), circle.popleft(), circle.popleft()]
    if DBG:
        print("pick up:", three_cups)

    dest = current_cup-1
    if dest == 0:
        dest = max_cup
    while dest in three_cups:
        dest = dest - 1
        if dest == 0:
            dest = max_cup
    if DBG:
        print("destination: ", dest)

    idest = circle.index(dest)
    circle.rotate(-idest-1)

    circle.extend(three_cups)

    icur = circle.index(current_cup)
    circle.rotate(-icur-1)

    if DBG:
        print("end cups: ", circle)

    return circle


def play_game(circle, total_moves, DBG=True):
    # game
    move_id = 1
    while (move_id <= total_moves):
        if DBG:
            print("-- move ", move_id, " --")
        circle = play_round(circle, move_id, DBG)
        move_id = move_id + 1

    return circle


def compute_order(circle):
    i_one = circle.index(1)

    circle.rotate(-i_one)

    circle.popleft()
    ret = ""
    for i in circle:
        ret = ret + str(i)

    return ret


def boom(input_val, DBG=True):
    circle = parse_cups(input_val, DBG)

    circle = play_game(circle, 100, DBG)

    if(DBG):
        print("== final ==")
        print(circle)

    order = compute_order(circle)

    return order


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

########


tt1 = "389125467"

test(tt1, "67384529", True)
# sys.exit()

#########

INPUT_FILE = "input-d22.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom("538914762", DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 1 = 54327968
