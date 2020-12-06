# coding: utf-8
import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time

def end_cur_group(groups, cur_group, nb_yes):
    groups.append(cur_group)
    nb_yes = nb_yes + len(cur_group)
    return nb_yes

def boom(input_val, DBG = True):
    groups = []

    cur_group = {}
    nb_yes = 0
    for line in input_val:
        if (line==''):
            nb_yes = end_cur_group(groups, cur_group, nb_yes)
            cur_group = {}
        else:
            for q in line:
                if not q in cur_group:
                    cur_group[q] = 0
                cur_group[q] = cur_group[q] + 1
    nb_yes = end_cur_group(groups, cur_group, nb_yes)

    return nb_yes

def test(cc=None, expected=None, DBG = False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc,DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected=="None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))    
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result)+ " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")
    return flag


t1="""abc

a
b
c

ab
ac

a
a
a
a

b"""
tt1 = t1.splitlines()
test(tt1,11,True)
#sys.exit()

INPUT_FILE="input-d06.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False) 
print(ret)

# part 1 = 6382