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

	if (DBG):print(ii)

	res = re.findall(r'\d+', ii)
	a = int(res[0])
	b = int(res[1])
	c = int(res[2])
	if (a+b<=c): return False
	if (b+c<=a): return False
	if (c+a<=b): return False
	return True

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="""5 10 25"""
tt = t1.splitlines()

test(tt[0],False,True) # 

INPUT_FILE="input-d03.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

nn=0
for tt in puzzle_input:
	result = function(tt,False)
	if (result == True):
		nn = nn+1
print(nn)


