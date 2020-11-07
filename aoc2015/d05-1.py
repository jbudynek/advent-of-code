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

	# 3 vowels
	re1 = r'([aeiou].*){3}'
	re11 = re.compile(re1)
	if re11.search(ii) == None:
		if(DBG): print("3w")
		return False

	# 2 letters repeated
	re2 = r'([a-z])\1'
	re22 = re.compile(re2)
	if re22.search(ii) == None:
		if(DBG): print("2")
		return False

	# not ab, cd, pq, or xy
	ss = ["ab", "cd", "pq", "xy"]
	for aa in ss:
		if aa in ii:
			if(DBG): print("forb")
			return False

	return True

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="ugknbfddgicrmopn"
test(t1,True,False) # 

t2="aaa"
test(t2,True,False) # 

t3="jchzalrnumimnmhp"
test(t3,False,True) # 

t4="haegwjzuvuyypxyu"
test(t4,False,True) # 

t5="dvszwmarrgswjxmb"
test(t5,False,True) # 


INPUT_FILE="input-d05.txt"

f = open(INPUT_FILE, "r")
puzzle_input = [line.rstrip('\n') for line in f]
f.close()


nn = 0
for pp in puzzle_input:
	#print("*" + str(pp) + "**")
	result = function(pp,False)
	if result == True:
	    nn = nn + 1
print(nn)

#################

