# coding: utf-8

import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
from collections import Counter
import time


def build_world(ii, DBG = True):
    world = {}
    xmin = ymin = 1000
    xmax = ymax = 0
    idx = ord('A')
    for line in ii:
        xy = line.split(",")
        xy = np.asarray(xy, dtype=np.int)
        if(DBG):print(xy,chr(idx))
        world[chr(idx)] = (xy[0],xy[1])
        xmin = min(xmin,xy[0])
        ymin = min(ymin,xy[1])
        xmax = max(xmax,xy[0])
        ymax = max(ymax,xy[1])
        idx = idx +1
    bbox = (xmin, xmax, ymin, ymax)
    if(DBG):print(bbox)
    if(DBG):print(world)
    return (world,bbox)

def manhattan_distance(x0,y0,x1,y1):
    return abs(x1-x0)+abs(y1-y0)

def count_area(world, bbox, DBG = True):
    xmin = bbox[0]
    xmax = bbox[1]
    ymin = bbox[2]
    ymax = bbox[3]
    areas = 0
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            total_dist = 0
            for key in world:
                target = world[key]
                dist = manhattan_distance(x,y,target[0],target[1])
                total_dist = total_dist + dist
            if (DBG) : print(x,y,total_dist,areas)
            if total_dist<10000:
                areas = areas + 1
    if (DBG):print(areas)
    return areas


def function(ii, DBG = True):

    # build world = put targets A B C D where they belong
    # find bounding box
    # loop on xy within bouding box
    # in each spot record closest target with Manhattan distance
    # count areas where distance < 1000

    (world, bbox) = build_world(ii, DBG)

    nb_areas = count_area(world, bbox, DBG)


    if(DBG):print(nb_areas)
    return nb_areas


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))

    result = str(function(cc,DBG))

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
tt1 = t1.splitlines()
#test(tt1,16,True) # 

#sys.exit()

INPUT_FILE="input-d06.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input,False) # 
print(ret)
