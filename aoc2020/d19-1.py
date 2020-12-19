# coding: utf-8
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
# from functools import reduce
# from math import log
#from itertools import product
import copy
import operator
import re
import string
import sys
import time

import numpy as np


def parse_rules_and_messages(input_val, DBG):
    rules = {}
    messages = []
    nl = len(input_val)
    idx = 0
    part = 0
    while(idx < nl):
        ii = input_val[idx]
        if ii == '':
            part = part+1
        elif part == 0:
            rr = ii.split(":")
            nr = int(rr[0])
            if '|' in rr[1]:
                rrr = rr[1].split("|")
                lhs = np.asarray(re.findall(r'\d+', rrr[0]), dtype=np.int)
                rhs = np.asarray(re.findall(r'\d+', rrr[1]), dtype=np.int)
                rules[nr] = (lhs, rhs)
            elif '"' in rr[1]:
                rules[nr] = rr[1][2]
            else:
                lhs = np.asarray(re.findall(r'\d+', rr[1]), dtype=np.int)
                rules[nr] = lhs
        elif part == 1:
            messages.append(ii)
        else:
            sys.exit("panic "+str(ii))
        idx = idx+1

    if DBG:
        print(rules)

    return (rules, messages)


def match(message, m_pos, rules, r_idx, DBG):
    r = rules[r_idx]
    if m_pos >= len(message):
        if DBG:
            print("too far!! test rule#", r_idx, "=", r, "m_pos=",
                  m_pos)
        return (False, m_pos)
    if DBG:
        print("test rule#", r_idx, "=", r, "m_pos=",
              m_pos, "message[m_pos]", message[m_pos])
    if isinstance(r, str):  # character
        ret = (r == message[m_pos])
        if DBG:
            if ret:
                print("match char rule ", r_idx)
            else:
                print("no match char rule ", r_idx)
        return (ret, m_pos+1)
    elif isinstance(r, tuple):  # N rules | P rules

        # test first set of N rules
        (ret_b, ret_p) = test_n_rules(message, r[0], r_idx, m_pos, rules, DBG)
        if ret_b:
            if DBG:
                print("match first part of | rule ", r_idx)
            return (ret_b, ret_p)

        # test second set of P rules
        (ret_b, ret_p) = test_n_rules(message, r[1], r_idx, m_pos, rules, DBG)
        if ret_b:
            if DBG:
                print("match second part of | rule ", r_idx)
            return (ret_b, ret_p)

        # no match
        if DBG:
            if DBG:
                print("no match | rule ", r_idx)
        return(False, m_pos)

    else:  # N rules
        (ret_b, ret_p) = test_n_rules(message, r, r_idx, m_pos, rules, DBG)
        if ret_b:
            if DBG:
                print("match n rule ", r_idx)
        else:
            if DBG:
                print("no match n rule ", r_idx)

        return (ret_b, ret_p)

    return (False, -1)


def test_n_rules(message, r, r_idx, m_pos, rules, DBG):
    rrr = 0
    cur_m_pos = m_pos
    while(rrr < len(r)):
        mm1 = False
        (mm1, new_m_pos) = match(message, cur_m_pos, rules, r[rrr], DBG)
        if not mm1:
            if DBG:
                print("no match rule ", r[rrr])
            return (False, m_pos)
        else:
            if DBG:
                print("match rule ", r[rrr])
        cur_m_pos = new_m_pos
        rrr = rrr + 1
    if DBG:
        print("match full rule ", r_idx)
    return (True, cur_m_pos)


def boom(input_val, DBG=True):
    (rules, messages) = parse_rules_and_messages(input_val, DBG)
    ret = 0
    for message in messages:
        if DBG:
            print(message)
        # ababbb
        # abbbab
        (mm, m_pos) = match(message, 0, rules, 0, DBG)
        if DBG:
            print("**", mm, m_pos, message)
        # aa=input()
        if mm and m_pos == len(message):
            ret = ret + 1

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


t1 = """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba"""

tt1 = t1.splitlines()
test(tt1, 2, False)
# sys.exit()

t1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
tt1 = t1.splitlines()
test(tt1, 2, False)
# sys.exit()

INPUT_FILE = "input-d19.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 184
