# coding: utf-8
import numpy as np
import re
import copy
import sys
import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time
from itertools import combinations

  
def boom(input_val, DBG = True):

    numbers = np.asarray(input_val, dtype=np.int)
    if DBG:print(numbers)

    window = 25

    for idx in range(window+1,len(numbers)):
        total = numbers[idx-1]
        found = False
        if DBG:print("looking for", total)
        candidates = numbers[idx-window-1:idx-1]
        if DBG:print("in", candidates)

        for (p,q) in combinations(candidates,2):
            if (p+q) == total:
                found = True
                if DBG:print("found", p, q)
                continue
        if found: 
            continue
        else:
            if DBG:print("total not found")
            return total
 
    return (-1)

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


t1="""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
tt1 = t1.splitlines()
#test(tt1,127,True)
#sys.exit()


INPUT_FILE="input-d09.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False) 
print(ret)

# part 1 = 257342611