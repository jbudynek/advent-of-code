# coding: utf-8
import numpy as np
import re
import copy
import sys
import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time

def create_world(rules, DBG = True):
    world = nx.DiGraph()

    # light red bags contain 1 bright white bag, 2 muted yellow bags.

    for rule in rules:
        words = rule.split(' ')
        node0_name = words[0]+' '+words[1]
        world.add_node(node0_name)
        if DBG: print(node0_name)
        i=4
        while i<len(words):
            node_name = words[i+1]+" "+words[i+2]
            if words[i]=="no": break
            node_weight = int(words[i])
            world.add_edge(node_name,node0_name,weight=node_weight)
            #world.add_edge(node0_name,node_name,weight=node_weight)
            i = i + 4
            if DBG: print(node_name,node_weight)
    
    if DBG: print(world.number_of_nodes(),world.number_of_edges(),list(world.nodes),list(world.edges))
    return world
            
def get_all_parents(node, world, DBG = True):
    up = list(world.predecessors(node))
    if DBG: print(node, up)
    if len(up)==0:
        return 1
    else:
        ret = 1
        for up_node in up:
            w = world.edges[up_node, node]["weight"]
            gap = get_all_parents(up_node, world, DBG)
            if DBG: print("* node ",node, "has parent", up_node, "with weight", w, "and all parents", gap)
            ret = ret + w * gap
            if DBG:print (node, ret)
        if DBG: print(ret)
        return ret

def boom(input_val, DBG = True):
    rules = input_val
    world = create_world(rules, DBG)
    nb_colors = 0

    node = "shiny gold" # RECURSE
    if DBG: print(node)
    nb_colors = get_all_parents(node,world,DBG)-1

    return nb_colors

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


t1="""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
tt1 = t1.splitlines()
test(tt1,32,True)
#sys.exit()

t1="""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
tt1 = t1.splitlines()
test(tt1,126,True)
#sys.exit()

INPUT_FILE="input-d07.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False) 
print(ret)

# part 2 = 8030