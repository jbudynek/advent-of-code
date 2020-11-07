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
kk = 0
ll = len(puzzle_input)
while kk<ll:
	tt1 = puzzle_input[kk]
	res = re.findall(r'\d+', tt1)
	a1 = int(res[0])
	b1 = int(res[1])
	c1 = int(res[2])

	tt2 = puzzle_input[kk+1]
	res = re.findall(r'\d+', tt2)
	a2 = int(res[0])
	b2 = int(res[1])
	c2 = int(res[2])

	tt3 = puzzle_input[kk+2]
	res = re.findall(r'\d+', tt3)
	a3 = int(res[0])
	b3 = int(res[1])
	c3 = int(res[2])

	result = function(str(a1)+" "+str(a2)+" "+str(a3),False)
	if (result == True):
		nn = nn+1
	result = function(str(b1)+" "+str(b2)+" "+str(b3),False)
	if (result == True):
		nn = nn+1
	result = function(str(c1)+" "+str(c2)+" "+str(c3),False)
	if (result == True):
		nn = nn+1
	kk = kk+3
print(nn)


