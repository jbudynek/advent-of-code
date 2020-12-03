# coding: utf-8
import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

def print_field(xyids, x,y , DBG=True):

    coords = xyids.keys()
    if(DBG): print(xyids)
    x_min = min(coords, key = lambda t: t[0])[0]-1
    x_max = max(coords, key = lambda t: t[0])[0]+1
    y_min = min(coords, key = lambda t: t[1])[1]-1
    y_max = max(coords, key = lambda t: t[1])[1]+1
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    delete_last_lines(21)

    for yy in range(y-10,y+11):
#    for yy in range(y_min,y_max+1):
        ss = ""
        for xx in range(x_min,x_max+1):
            if (xx==x) and (yy==y) and  (xx,yy) in xyids:
                 ss +='💥'
            elif (xx==x) and (yy==y):
                 ss +='🏂'
            elif (xx,yy) in xyids:
                ##########
                ss += '🎄'
            else:
                ss += "  "
        print(ss)
    time.sleep(0.3)

def create_world(ccc, DBG=True):
    field = {}
    x=-1
    y=-1
    for line in ccc:
        y+=1
        x=-1
        for c in line:
            x+=1
            if c=='.': 
                continue
            else: 
                field[(x,y)]=c

    if DBG:print(field)    
    return (field)
    
def trees(x_max,y_max,world,dx,dy,DBG=False):
    count_trees = 0
    cur_x=0
    cur_y=0
    while cur_y<y_max:
        if(DBG):print_field(world,cur_x,cur_y,False)
        if (cur_x,cur_y) in world:
            count_trees = count_trees + 1
        cur_x = (cur_x + dx) % x_max
        cur_y = cur_y + dy
    return count_trees

def boom(input_val, DBG = True):
    world = create_world(input_val, DBG)

    x_max = len(input_val[0])
    y_max = len(input_val)

    product = 1
    for (dx,dy) in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
        product = product * trees(x_max,y_max,world,dx,dy,DBG)

    return product

def test(cc=None, expected=None, DBG = False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc,DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected=="None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))    
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result)+ " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")
    return flag


t1="""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
tt1 = t1.splitlines()
#test(tt1,336,True)
#sys.exit()

INPUT_FILE="input-d03.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# set DBG to True for animation
ret = boom(puzzle_input, DBG = True) 
print(ret)

# part 2 = 5140884672