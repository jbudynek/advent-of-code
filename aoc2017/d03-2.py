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
    world = {}
    cur_x=0
    cur_y=0

    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    cur_dir = 0

    delta_0 = 1
    delta_1 = 1
    last_turn = 0

    for i in range(1,ii):
        if (i == 1):
            world[(cur_x,cur_y)] = 1
        else:
            world[(cur_x,cur_y)] = 0

        if (cur_x+1,cur_y) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x+1,cur_y)]
        if (cur_x+1,cur_y+1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x+1,cur_y+1)]
        if (cur_x,cur_y+1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x,cur_y+1)]
        if (cur_x-1,cur_y+1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x-1,cur_y+1)]
        if (cur_x-1,cur_y) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x-1,cur_y)]
        if (cur_x-1,cur_y-1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x-1,cur_y-1)]
        if (cur_x,cur_y-1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x,cur_y-1)]
        if (cur_x+1,cur_y-1) in world:
            world[(cur_x,cur_y)] = world[(cur_x,cur_y)] + world[(cur_x+1,cur_y-1)]

        if(DBG): print(cur_x,cur_y, world[(cur_x,cur_y)])

        if (world[(cur_x,cur_y)])>ii:
            return (world[(cur_x,cur_y)])

        cur_x = cur_x + directions[cur_dir][0]
        cur_y = cur_y + directions[cur_dir][1]
        if (i-last_turn==delta_0):
            cur_dir = (cur_dir + 1) % len(directions)
            last_turn = i
            if(delta_0==delta_1):
                delta_0 = delta_1
                delta_1 = delta_1+1
            else:
                delta_0 = delta_1
                delta_1 = delta_1
    return abs(cur_x)+abs(cur_y)


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


test(1,1,True) # 
test(2,1,True) # 
test(3,2,True) # 
test(4,4,True) # 
test(5,5,True) # 

INPUT_FILE="input-d02.txt"

puzzle_input = 347991


result = function(puzzle_input,False)
print(result)

#################

