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


def update_rules_to_field(rules, rule_to_fields, vt, DBG=True):
    for idx in range(len(vt)):
        nn = vt[idx]
        for r in rules:
            (name, l0, h0, l1, h1) = r
            if not ((nn >= l0 and nn <= h0) or (nn >= l1 and nn <= h1)):
                if DBG:
                    print("**", name, l0, h0, l1, h1,
                          "does not match", nn, "at idx", idx)
                if r in rule_to_fields:
                    if idx in rule_to_fields[r]:
                        rule_to_fields[r].remove(idx)
        if DBG:
            for (r, v) in rule_to_fields.items():
                print(r, v)

    return rule_to_fields


def boom(input_val, DBG=True):

    # parse world
    rules = []
    my_ticket = []
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
        if (ppp == 1):
            my_ticket = parse_ticket(ii, DBG)
        if (ppp == 2):
            nearby_tickets.append(parse_ticket(ii, DBG))
        idx = idx + 1

    # get valid tickets only
    valid_tickets = []
    for t in nearby_tickets:
        err = get_invalidity(t, rules, DBG)
        if err == 0:
            valid_tickets.append(t)

    # initially all rules can apply to all fields
    rule_to_fields = {}
    all_indexes = list(range(len(my_ticket)))
    for r in rules:
        rule_to_fields[r] = all_indexes.copy()
    # each valid ticket helps updating which rule apply to which field
    for vt in valid_tickets:
        rule_to_fields = update_rules_to_field(rules, rule_to_fields, vt, DBG)

    # remove duplicates, by finding rules that have only one possible field and removing it from elsewhere
    cont = True
    while(cont):
        cont = False
        for r in rule_to_fields.keys():
            fields = rule_to_fields[r]
            if len(fields) == 1:
                field = fields[0]
                for r2 in rule_to_fields.keys():
                    fields2 = rule_to_fields[r2]
                    if field in fields2 and len(fields2) > 1:
                        fields2.remove(field)
        for (r, fields) in rule_to_fields.items():
            if len(fields) > 1:
                cont = True

    # we should have one rule per field by now
    if DBG:
        print("***", rule_to_fields)

    # find the ones that start with "departure" and multiply
    ret = 1
    for (r, fields) in rule_to_fields.items():
        (name, l0, h0, l1, h1) = r
        field = fields[0]
        if DBG:
            print("rule ", r)
        if DBG:
            print("field ", field)
        if DBG:
            print("my ticket value ", my_ticket[field])
        if name.startswith("departure"):
            ret = ret * my_ticket[field]
            if DBG:
                print("*ret ", ret)

    return ret


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
departure row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
tt1 = t1.splitlines()
test(tt1, 7, True)
# sys.exit()

INPUT_FILE = "input-d16.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 5865723727753
