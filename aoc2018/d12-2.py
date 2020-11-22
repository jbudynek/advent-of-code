# coding: utf-8
import numpy as np
import re
import copy
import sys
import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
from collections import Counter
from collections import deque
import time

def parse_input(ii, DBG=True):
    world = {}
    index = 0
    init_state = ii[0]
    for c in range(15, len(init_state)):
        if init_state[c]=="#":
            world[index]=1
            index = index+1
        elif init_state[c]==".":
            world[index]=0
            index = index+1
        else:
            print("**"+init_state[c]+"**")
            sys.exit()
    if DBG: print(ii[0], world)

    rules = []
    rr = len(ii)
    for ri in range(2,rr):
        raw_rule = ii[ri]
        rule_lhs=[]
        for idx in range(0,5):
            if raw_rule[idx]=="#":
                rule_lhs.append(1)
            elif raw_rule[idx]==".":
                rule_lhs.append(0)
            else:
                print("**"+raw_rule[idx]+"**")
                sys.exit()
        if raw_rule[9]=="#":
            rule_rhs=1
        elif raw_rule[9]==".":
            rule_rhs=0
        rules.append((rule_lhs,rule_rhs))
        if DBG: print(raw_rule, rule_lhs,rule_rhs)

    return (world,rules)

def match(world, index, rule, DBG = True):
    world_five_array = []
    if DBG: print(rule)
    for idx in range(-2,3):
        if (index+idx) in world:
            world_five_array.append(world[index+idx])
        else:
            world_five_array.append(0)

    if DBG: print(world_five_array)

    if world_five_array == rule[0]:
        return (True, rule[1])
    else:
        return (False, None)

def count_plants(world):
    count =0
    sum_idx = 0
    for k in world:
        if world[k] == 1:
            count = count+1
            sum_idx = sum_idx + k
    return(count, sum_idx)

def world_str(world):
    out = ""
    for k in world:
        if (world[k]==1):
            out = out +"#"
        elif (world[k]==0):
            out = out +"."
    (ct,sum_idx) = count_plants(world)
    return out + " " + str(ct) + " "+ str(sum_idx)
    

def function(ii, DBG = True):

    # parse initial state into world
    # parse rules
    (world, rules) = parse_input(ii, DBG)

    #if DBG: print(match(world,0,rules[1]))

    if DBG: print("0: "+world_str(world))

    # loop on xxx generations
    # apply rules left to right, into a new world
    # copy new world into world
    # --> print out sum of indexes, and delta from previous generation
    # (print out state, count plants)

    # ** we see that delta is always the same after some generations 
    # so we can apply a formula (see below)

    last_sum_idx = count_plants(world)[1]

    for gen in range(1,135):
        new_world = {}
        for index in range(-2, len(world)+1):
            #new_world[index] = 0
            for rule in rules:
                mm = match(world,index,rule,False)
                if mm[0]==True:
                    new_world[index] = mm[1]
                    continue
        #if DBG: print(str(gen)+": "+world_str(new_world))
        world = new_world

        (count, sum_idx) = count_plants(world)
        delta = sum_idx-last_sum_idx
        last_sum_idx = sum_idx
        print(gen, count, sum_idx, delta)

    # gen 128 count 78 sum_idx 12196 delta 247
    # gen 129 count 78 sum_idx 12274 delta 78
    # gen 130 count 78 sum_idx 12352 delta 78

    # sum_idx(gen) = 12196 + ((gen-128) * 78)

    return count_plants(world)[1]

def test(cc=None, expected=None, DBG = False):
    start_millis = int(round(time.time() * 1000))
    result = function(cc,DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected=="None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))    
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")
    return flag


t1="""initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""
tt1 = t1.splitlines()
#test(tt1,325,True) 
#sys.exit()

INPUT_FILE="input-d12.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input, True) 
print(ret)

print(12196 + ( (50000000000-128) * 78))

# 3900000002212
