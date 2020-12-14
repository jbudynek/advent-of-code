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


def boom(input_val, DBG=True):
    # mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    # mem[8] = 11

    mask = []
    mem = {}
    for instr in input_val:
        if "mask" in instr:
            mask = instr.split(' ')[2]
        else:
            nn = np.asarray(re.findall(r'\d+', instr), dtype=np.int)
            address = nn[0]
            val = nn[1]
            address_b_0 = list("{0:036b}".format(address))
            if DBG:
                print("addr", ''.join(address_b_0))
                print("mask", mask)
            # address can change with "floating" bits so we will keep them in an array
            addresses = []
            addresses.append(address_b_0)
            for i in range(len(mask)):
                # 1 or 0
                if mask[-1-i] == '1':
                    for address_b in addresses:
                        address_b[-1-i] = mask[-1-i]
                elif mask[-1-i] == '0':
                    pass
                # deal with "X" : put 0, copy all adresses (array doubles in size), then put 1
                else:
                    for address_b in addresses:
                        address_b[-1-i] = '0'
                    for k in range(len(addresses)):
                        address_b = addresses[k]
                        address_b_n = address_b.copy()
                        address_b_n[-1-i] = '1'
                        addresses.append(address_b_n)

            # write in mem
            for address_b in addresses:
                address_b = ''.join(address_b)
                address = int(address_b, 2)
                if DBG:
                    print(address_b, address, val)
                mem[address] = val

    return sum(mem.values())


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


t1 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
tt1 = t1.splitlines()
test(tt1, 208, True)
# sys.exit()

INPUT_FILE = "input-d14.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 3505392154485
