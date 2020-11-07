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

def find_abba(iterator, DBG = True):
	for match in iterator:
		if(DBG):print("looking for ABBA in " +match.group())
		p = re.compile(r'(([a-z])([a-z])\3\2)')
		abbas = p.findall(match.group())
		for abbatuple in abbas:
			abba=abbatuple[0]
			if(abba[0]!=abba[1]):
				if(DBG): print("found ABBA "+abba)
				return True
	return False

def function(ii, DBG = True):

	if(DBG):print("full address "+ii)

	# search for ABBA not in brackets

	# search for ABBA inside bracket
	re1 = r'\[[a-z]*?([a-z])([a-z])\2\1[a-z]*?\]'
	re11 = re.compile(re1)
	iterator = re11.finditer(ii)
	if (find_abba(iterator,DBG)): 
		if(DBG):print("abba in brackets")
		return False

	# ok there's no ABBA inside brackets

	# search for ABBA before first opening bracket
	re1 = r'^[a-z]*?([a-z])([a-z])\2\1[a-z]*?\['
	re11 = re.compile(re1)
	iterator = re11.finditer(ii)
	if (find_abba(iterator,DBG)): 
		return True

	# search for ABBA after last closing bracket
	re1 = r'\][a-z]*?([a-z])([a-z])\2\1[a-z]*?$'
	re11 = re.compile(re1)
	iterator = re11.finditer(ii)
	if (find_abba(iterator,DBG)): 
		return True

	# search for ABBA between brackets
	re1 = r'\][a-z]*?([a-z])([a-z])\2\1[a-z]*?\['
	re11 = re.compile(re1)
	iterator = re11.finditer(ii)
	if (find_abba(iterator,DBG)): 
		return True

	# well then
	if(DBG): print("found no ABBA")
	return False

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="abba[mnop]qrst"
test(t1,True,True) # 

t2="abcd[bddb]xyyx"
test(t2,False,True) # 


t3="aaaa[qwer]tyui"
test(t3,False,True) # 

t4="ioxxoj[asdfgh]zxcvbn"
test(t4,True,True) # 

INPUT_FILE="input-d07.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
for pp in puzzle_input:
	result = function(pp,False)
	if result == True:
	    nn = nn + 1
	kk = kk+1
	#if (kk==10):break
print(nn)

#################

