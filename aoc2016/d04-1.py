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
from collections import Counter


def function(ii, DBG = True):

	if (DBG):print(ii)
	pp =re.split("[\[\]]+", ii)
	checksum=pp[1]
	if (DBG):print(checksum)
	pp =re.split("[\[\]-]+", ii)
	value = pp[-3]
	if (DBG):print(value)
	pp =re.split(value, ii)
	code = pp[0]
	if (DBG):print(code)
	counts=Counter(code)
	counts['-']=0
	if (DBG):print(counts)


	ttt = dict(sorted(counts.items(), key=lambda x: (x[1],-ord(x[0])), reverse=True))
	mycheksum=''.join(list(ttt.keys())[0:5])
	return (checksum==mycheksum, int(value))

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="aaaaa-bbb-z-y-x-123[abxyz]"
test(t1,(True,123),True) # 
t1="a-b-c-d-e-f-g-h-987[abcde]"
test(t1,(True,987),True) # 
t1="not-a-real-room-404[oarel]"
test(t1,(True,404),True) # 
t1="totally-real-room-200[decoy]"
test(t1,(False,200),True) # 

INPUT_FILE="input-d04.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

nn=0
for tt in puzzle_input:
	(result,value) = function(tt,False)
	if (result == True):
		nn = nn+value
print(nn)

##########

def decrypt(ss,ii):
	o = ''
	for c in ss:
		if (c=='-'):
			o = o + ' '
		else:
			o = o + chr(((ord(c)-ord('a')+ii)%26)+ord('a'))
	return(o)

for tt in puzzle_input:
	(result,value) = function(tt,False)
	if (result == True):
		dname = decrypt(tt,value)
		print(dname + "**"+str(value))
		if 'north' in dname:
			sys.exit()

