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

def parse(world, ss, DBG = True):

	res = re.findall(r'\d+', ss)
	if(DBG): print(res)

	x0=int(res[0])
	y0=int(res[1])
	x1=int(res[2])
	y1=int(res[3])
	
	if (ss.startswith('turn off')):
		world[x0:x1+1,y0:y1+1] = 0
	elif (ss.startswith('turn on')):
		world[x0:x1+1,y0:y1+1] = 1
	elif (ss.startswith('toggle')):
		world[x0:x1+1,y0:y1+1] = np.absolute(world[x0:x1+1,y0:y1+1] - 1)
	else:
		print(ss)
		sys.exit()
	return world


INPUT_FILE="input-d06.txt"

f = open(INPUT_FILE, "r")
puzzle_input = [line.rstrip('\n') for line in f]
f.close()

#turn off 199,133 through 461,193
#toggle 322,558 through 977,958
#turn on 226,196 through 599,390

world = np.full((1000, 1000), 0)
print(world)
print(np.count_nonzero(world))

#world = parse(world, "turn on 0,0 through 999,999", True )
#world = parse(world, "turn off 499,499 through 500,500", True)
#world = parse(world, "toggle 0,0 through 999,0", True)
#print(world)
#print(np.count_nonzero(world))

nn = 0
for pp in puzzle_input:
	#print("*" + str(pp) + "**")
	world = parse(world, pp, True)

print(world)
print(np.count_nonzero(world))

#################

