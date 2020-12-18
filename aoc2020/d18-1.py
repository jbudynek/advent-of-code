# coding: utf-8
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
# from functools import reduce
# from math import log
import copy
import operator
import re
import sys
import time
from itertools import product
from operator import add, mul

import numpy as np

operators = {
    '+': add,
    '*': mul,
}


def find_parens(s):
    ret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            ret[pstack.pop()] = i

    return ret


def calculate(s, DBG=True):
    if DBG:
        print(s)

    parens = find_parens(s)

    lhs = 0
    ret = 0
    operator = '+'
    i = 0
    while i < len(s):
        if s[i].isdigit():
            lhs = int(s[i])
            ret = operators[operator](ret, lhs)
            i = i+1
        elif s[i] in operators.keys():
            operator = s[i]
            i = i+1
        elif s[i] == '(':
            ss = s[i+1:parens[i]]
            if DBG:
                print(ss)
            lhs = calculate(ss, DBG)
            ret = operators[operator](ret, lhs)
            i = parens[i] + 1
        elif s[i] == ' ':
            i = i+1
            pass
    return ret


def boom(input_val, DBG=True):

    ret = 0
    for expr in input_val:
        value = calculate(expr, DBG)
        ret = ret + value

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


t1 = """1 + 2 * 3 + 4 * 5 + 6"""
tt1 = t1.splitlines()
test(tt1, 71, True)
# sys.exit()

t1 = """1 + (2 * 3) + (4 * (5 + 6))"""
tt1 = t1.splitlines()
test(tt1, 51, True)
# sys.exit()

t1 = """2 * 3 + (4 * 5)"""
tt1 = t1.splitlines()
test(tt1, 26, True)
# sys.exit()
t1 = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""
tt1 = t1.splitlines()
test(tt1, 437, True)
# sys.exit()
t1 = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
tt1 = t1.splitlines()
test(tt1, 12240, True)
# sys.exit()
t1 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
tt1 = t1.splitlines()
test(tt1, 13632, True)
# sys.exit()

INPUT_FILE = "input-d18.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 650217205854
