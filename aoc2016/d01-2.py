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

v_up = (0,1)
v_right = (1,0)
v_down = (0,-1)
v_left = (-1,0)

directions = [v_up,v_right,v_down,v_left]
#turn_left = [v_up,v_left,v_down,v_right]

def function(ii, DBG = True):

	visited = {}

	moves = ii.split(', ')

	cur_x=0
	cur_y=0
	cur_dir=0

	visited[(cur_x,cur_y)] = 1

	for move in moves:
		dir = move[0:1]
		blocks = int(move[1:])
		if (dir=='R'):
			cur_dir = ((cur_dir+1) %4)
		else:
			cur_dir = ((cur_dir-1) %4)
		for kk in np.arange(blocks):
			cur_x = cur_x + directions[cur_dir][0]
			cur_y = cur_y + directions[cur_dir][1]
			if (cur_x,cur_y) in visited:
				return abs(cur_x)+abs(cur_y)
			visited[(cur_x,cur_y)] = 1

	return abs(cur_x)+abs(cur_y)

def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="R8, R4, R4, R8"
test(t1,4,False) # 

INPUT_FILE="input-d01.txt"

f = open(INPUT_FILE, "r")
puzzle_input = [line.rstrip('\n') for line in f]
f.close()

for pp in puzzle_input:
	#print("*" + str(pp) + "**")
	result = function(pp,False)
	print(result)

