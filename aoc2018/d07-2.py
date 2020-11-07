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
import time


def build_world(ii, DBG = True):
    world = nx.DiGraph()
    for line in ii:
        # "Step C must be finished before step A can begin"
        node_from = list(line)[5]
        node_to = list(line)[36]
        if(DBG):print(node_from,node_to)
        world.add_node(node_from)
        world.add_node(node_to)
        world.add_edge(node_from,node_to)
    if(DBG):print(world.edges)
    return world


start_time = {}

def get_start_time(node, DBG = True):
    return start_time[node]

def get_duration(node, DBG = True):
    return ord(str(node)[0])-ord('A')+1+OVERHEAD


worker_to_node = {}
def get_current_node(worker, DBG = True):
    if worker in worker_to_node:
        return worker_to_node[worker]
    else:
        return None

worker_status = {}
def set_worker_status(worker, status, DBG = True):
    worker_status[worker] = status

def get_worker_status(worker, DBG = True):
    if not worker in worker_status:
        worker_status[worker] = "idle"
    return worker_status[worker]

# status = "idle","working"
def update_status(worker, node, tick, world, DBG = True):
    if (DBG): print(worker, node, tick)
    status = get_worker_status(worker, DBG)
    if (status=="working"):
        if (DBG): print("working "+node)
        delta = tick - get_start_time(node)
        if (DBG): print("delta ",delta)
        if (delta >= get_duration(node)):
            if (DBG): print("node "+node+ " done")
            worker_to_node[node] = None
            set_worker_status(worker, "idle")
            world.remove_node(node)
            return("idle")
    return status

def start_job(worker, node,tick, world, DBG = True):
    if (DBG): print("**start_job ",worker,node,tick)
    worker_to_node[worker] = node
    start_time[node] = tick
    set_worker_status(worker,"working")

def get_next_available_node(world, DBG = True):
    # find nodes without parent
    ret = []
    for node in world.nodes:
        if len(list(world.predecessors(node)))==0:
            if not node in worker_to_node.values():
                ret.append(node)
    if (DBG): print("available "+str(ret))
    if len(ret)==0:
        return None
    else:
        return ret[0]

def is_done(world, DBG = True):
    return world.number_of_nodes() == 0
    
WORKERS =  5
OVERHEAD =  60

def function(ii, DBG = True):

    # build world = build DAG 
    # topological sort

    # build N graphs (1 per worker)
    # ticks
    # on each graph label "doing" or "done" (propagate to other graphs)
    # when possible, take a node
    # log when "done"
    # when all is done ... we're done

    world = build_world(ii,DBG)

    #ts = list(nx.lexicographical_topological_sort(world))


    tick = 0
    # 

    while (True):
        for worker in range(WORKERS):
            if(DBG): print ("*worker "+str(worker))
            node = get_current_node(worker, DBG)
            if(DBG): print ("*node "+str(node))
            status = update_status(worker, node, tick, world, DBG)
            if(DBG): print ("*status "+status)
            if (status=="idle"):
                node = get_next_available_node(world, DBG)
                if(DBG): print ("*available "+str(node))
                if not node == None:
                    start_job(worker,node,tick, world, DBG)
        if(is_done(world, DBG)):
            return tick
        tick = tick+1

    return -1


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))

    result = str(function(cc,DBG))

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
tt1 = t1.splitlines()
#test(tt1,15,True) # 

#sys.exit()

INPUT_FILE="input-d07.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input,True) # 
print(ret)

# 230 LOW
