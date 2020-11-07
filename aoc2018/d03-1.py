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


def function(ii, DBG = True):
    ret = 0
    for c in ii:
        if ii[c] == 'X': ret = ret + 1
    return ret


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


def process_claim(world, line, DBG=True):
    nbs = re.findall(r'\d+', line)
    claim = str(nbs[0])
    x = int(nbs[1])
    y = int(nbs[2])
    w = int(nbs[3])
    h = int(nbs[4])
    for xx in range(x,x+w):
        for yy in range(y,y+h):
            coord = (xx,yy)
            if coord in world:
                world[coord] = 'X'
            else:
                world[coord] = claim
    return world

def build_world():
    world = {}
    return world

def process_all_claims(all_claims,DBG=True):
    world = build_world()
    for line in all_claims:
        world = process_claim(world, line)
        if(DBG):print(world)
    return world



t1="""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""
tt1 = t1.splitlines()
world = process_all_claims(tt1,True)
test(world,4,True) # 


INPUT_FILE="input-d03.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


world = process_all_claims(puzzle_input,False)
overlap = function(world,False) # 
print(overlap)

#################

