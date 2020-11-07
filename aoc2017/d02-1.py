# coding: utf-8

import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
import time


def function(ii, DBG = True):

	numbers = ii.split()
	x = np.array(numbers)
	y = x.astype(np.int)

	return np.amax(y) - np.amin(y)


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="5 1 9 5"
test(t1,8,True) # 

t2 = "7 5 3"
test(t2,4,True) # 

t3 = "2 4 6 8"
test(t3,6,True) # 

INPUT_FILE="input-d02.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
for pp in puzzle_input:
	result = function(pp,False)
	nn = nn + result
	kk = kk+1
	#if (kk==10):break
print(nn)

#################

