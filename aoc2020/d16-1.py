# coding: utf-8
import copy
import operator
import re
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time

import numpy as np

# from functools import reduce
# from math import log


def parse_rule(ii, DBG=True):
    # class: 1-3 or 5-7
    ww = ii.split(":")
    name = ww[0]
    w = ww[1].split(" ")
    r0 = w[1].split("-")
    l0 = int(r0[0])
    h0 = int(r0[1])
    r1 = w[3].split("-")
    l1 = int(r1[0])
    h1 = int(r1[1])
    if DBG:
        print(name, l0, h0, l1, h1)
    return (name, l0, h0, l1, h1)


def parse_ticket(ii, DBG=True):
    ii = ii.split(",")
    ticket = np.asarray(ii, dtype=np.int)
    if DBG:
        print(ticket)
    return ticket


def get_invalidity(t, rules, DBG=True):
    inv = 0
    for nn in t:
        valid = False
        for r in rules:
            (name, l0, h0, l1, h1) = r
            if not ((nn >= l0 and nn <= h0) or (nn >= l1 and nn <= h1)):
                if DBG:
                    print(nn, name, l0, h0, l1, h1, "*", nn)
            else:
                valid = True
        if not valid:
            inv = inv + nn
            if DBG:
                print("**", inv)

    return inv


def boom(input_val, DBG=True):

    rules = []
    #my_ticket = []
    nearby_tickets = []
    ppp = 0
    idx = 0
    while idx < len(input_val):
        ii = input_val[idx]
        if (ii == ""):
            ppp = ppp + 1
            idx = idx + 2
            continue
        if (ppp == 0):
            rules.append(parse_rule(ii, DBG))
        elif (ppp == 1):
            #my_ticket = 
            parse_ticket(ii, DBG)
        elif (ppp == 2):
            nearby_tickets.append(parse_ticket(ii, DBG))
        idx = idx + 1

    total = 0
    for t in nearby_tickets:
        err = get_invalidity(t, rules, DBG)
        total = total + err

    return total


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + str(flag) + " -> expected " + expected)
    print((stop_millis-start_millis), "ms", int((stop_millis-start_millis) /
                                                1000), "s", int((stop_millis-start_millis)/1000/60), "min")
    return flag


t1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
tt1 = t1.splitlines()
test(tt1, 71, True)
# sys.exit()

INPUT_FILE = "input-d16.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 25895
