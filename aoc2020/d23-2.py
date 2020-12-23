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
from timeit import default_timer as timer

import numpy as np

# deque is insufficient here as we need to look for "destination"
# instead, use a manual implementation of linked list with class Cup as node, that points to next Cup
# along with a dict that maps label to Cup (for fast destination lookup)
# runs in ~17 seconds on my computer


class Cup:

    def __init__(self, label):
        self.label = label
        self.next = None


def parse_cups(input_val, DBG):
    top_of_circle = None
    label_to_cup = {}

    prev_cup = None
    for ii in input_val:
        iii = int(ii)
        cup = Cup(iii)
        if top_of_circle == None:
            top_of_circle = cup
        label_to_cup[iii] = cup
        if not prev_cup == None:
            prev_cup.next = cup
        prev_cup = cup

    for ii in range(10, 1000001):
        cup = Cup(ii)
        prev_cup.next = cup
        label_to_cup[ii] = cup
        prev_cup = cup

    prev_cup.next = top_of_circle

    return (top_of_circle, label_to_cup)


def play_round(cur_cup, label_to_cup, move_id, DBG):
    if DBG:
        if(move_id % 1000000 == 0):
            print(move_id)

    max_cup = 1000000

    # get the three cups out, and their labels
    three_cups = [cur_cup.next, cur_cup.next.next, cur_cup.next.next.next]
    three_cups_labels = [three_cups[0].label,
                         three_cups[1].label, three_cups[2].label]

    # close circle
    cur_cup.next = cur_cup.next.next.next.next

    # what dest?
    dest_label = cur_cup.label - 1
    if dest_label == 0:
        dest_label = max_cup
    while dest_label in three_cups_labels:
        dest_label = dest_label - 1
        if dest_label == 0:
            dest_label = max_cup

    # get dest cup and re-wire to insert the three cups
    dest_cup = label_to_cup[dest_label]
    three_cups[2].next = dest_cup.next
    dest_cup.next = three_cups[0]

    # increment current cup
    cur_cup = cur_cup.next

    return (cur_cup, label_to_cup)


def play_game(top_of_circle, label_to_cup, total_moves, DBG=True):
    # game
    move_id = 1
    cur_cup = top_of_circle
    while (move_id <= total_moves):
        (cur_cup, label_to_cup) = play_round(
            cur_cup, label_to_cup,  move_id, DBG)
        move_id = move_id + 1

    return label_to_cup


def compute_product(label_to_cup, DBG):
    cup_one = label_to_cup[1]

    cup_one_next = cup_one.next.label
    cup_one_next_next = cup_one.next.next.label

    if DBG:
        print(cup_one_next, cup_one_next_next)

    return cup_one_next*cup_one_next_next


def boom(input_val, DBG=True):
    if DBG:
        print("creating circle...")
    (top_of_circle, label_to_cup) = parse_cups(input_val, DBG)

    if DBG:
        print("circle created")

    label_to_cup = play_game(top_of_circle, label_to_cup, 10000000, DBG)
    order = compute_product(label_to_cup, DBG)

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
test(tt1, 149245887792, True)
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

# part 2 = 157410423276
