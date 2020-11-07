# coding: utf-8

import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
from collections import Counter
import time


def function(ii, DBG = True):

    ii = np.asarray(ii, dtype=np.int)
    print(ii)

    cur_index=0
    cur_step=0
    while(cur_index<len(ii)):
        value = ii[cur_index]
        if(value>=3):
            ii[cur_index] = value-1
        else:
            ii[cur_index] = value+1
        cur_index = cur_index+value
        cur_step = cur_step+1

    if(DBG):print(ii)
    return cur_step


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="""0
3
0
1
-3"""
t1 = t1.splitlines()
test(t1,10,True) # 


INPUT_FILE="input-d05.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


result = function(puzzle_input,False)
print(result)

#################

