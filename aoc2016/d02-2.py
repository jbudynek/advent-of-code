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


keyboard = [
['0','0','D','0','0'],
['0','A','B','C','0'],
['5','6','7','8','9'],
['0','2','3','4','0'],
['0','0','1','0','0'],
]

def min_max(nn, mini, maxi):
	if nn<mini:
		return mini
	elif nn>maxi:
		return maxi
	else:
		return nn

def function(ii, DBG = True):

	if (DBG):print(ii)

	out = ""
	cur_x = 0
	cur_y = 2

	for iii in ii:

		for dir in iii:
			if (dir=='U'):
				cur_y_new = min_max((cur_y+1),0,4)
				if(keyboard[cur_y_new][cur_x]!='0'):
					cur_y=cur_y_new
			elif (dir=='D'):
				cur_y_new = min_max((cur_y-1),0,4)
				if(keyboard[cur_y_new][cur_x]!='0'):
					cur_y=cur_y_new
			elif (dir=='L'):
				cur_x_new = min_max((cur_x-1),0,4)
				if(keyboard[cur_y][cur_x_new]!='0'):
					cur_x=cur_x_new
			elif (dir=='R'):
				cur_x_new = min_max((cur_x+1),0,4)
				if(keyboard[cur_y][cur_x_new]!='0'):
					cur_x=cur_x_new
			else:
				print("***"+str(dir)+"***")
				sys.exit()
		out = out + str(keyboard[cur_y][cur_x])
	return out

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="""ULL
RRDDD
LURDL
UUUUD"""
tt = t1.splitlines()

test(tt,'5DB3',True) # 

INPUT_FILE="input-d02.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

result = test(puzzle_input,0,False)

