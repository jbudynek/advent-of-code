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

	lii = len(ii)
	ret=0

	k=0

	while(k<lii):
		if (ii[k] == ii[(k+lii//2)%lii]):
			ret = ret + int(ii[k])
		k = k+1

	return(ret)



def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="1122"
test(t1,3,True) # 

t2="1111"
test(t2,4,True) # 

t3="1234"
test(t3,0,True) # 

t4="91212129"
test(t4,9,True) # 

INPUT_FILE="input-d01.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


result = function(puzzle_input[0],False)
print(result)

#nn = 0
#kk = 0
#for pp in puzzle_input:
#	result = function(pp[0],False)
#	if result == True:
#	    nn = nn + 1
#	kk = kk+1
#	#if (kk==10):break
#print(nn)

#################

