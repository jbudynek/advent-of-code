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
    delta = np.abs(ord('A')-ord('a'))
    idx = 0
    list_ii = np.array(list(ii))
    while(idx<len(list_ii)-1):
        if( np.abs(ord(list_ii[idx])-ord(list_ii[idx+1])) == delta):
            list_ii = np.delete(list_ii,idx)
            list_ii = np.delete(list_ii,idx)
            idx = max(0,idx - 2)
        else:
            idx = idx+1
    if (DBG): print("***"+''.join(list_ii)+'***')
    ret = len(list_ii)
    return ret


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="dabAcCaCBAcCcaDA"
test(t1,10,True) # 

#sys.exit()

INPUT_FILE="input-d05.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
f.close()
puzzle_input = contents.rstrip()

ret = function(puzzle_input,True) # 
print(ret)
