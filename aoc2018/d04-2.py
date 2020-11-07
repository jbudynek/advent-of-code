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


def build_world():
    world = {}
    return world

def process_nap(world, cur_guard, falls_asleep,wakes_up, DBG=True):
    if cur_guard not in world:
        world[cur_guard] = np.zeros(60,np.int)
    world[cur_guard][falls_asleep:wakes_up] =  world[cur_guard][falls_asleep:wakes_up]+1
    if(DBG):print(cur_guard, world[cur_guard])
    return world


def find_most_slept_minute(world):

    # find highest slept minute

    most_slept = -1
    most_slept_minute = -1
    longest_sleeper = -1

    for sleeper in world:
        naps = world[sleeper]
        slept = np.max(naps)
        if slept>most_slept:
            most_slept = slept
            longest_sleeper = sleeper
            most_slept_minute = np.argmax(naps)
    return (longest_sleeper, most_slept_minute)

def process_schedule(all_lines,DBG=True):
    world = build_world()
    all_lines = np.sort(all_lines)
    if(DBG): print(all_lines[0:20])
    #sys.exit()
    cur_guard = -1
    begins_shift = -1
    falls_asleep = -1
    wakes_up = -1
    for line in all_lines:
        nbs = re.findall(r'\d+', line)
        if("begins shift" in line):
            cur_guard = str(nbs[5])
            begins_shift = int(nbs[4])
        elif ("falls asleep" in line):
            falls_asleep = int(nbs[4])
        elif ("wakes up" in line):
            wakes_up = int(nbs[4])
            if(DBG):print(cur_guard,falls_asleep,wakes_up)
            world = process_nap(world, cur_guard, falls_asleep,wakes_up,DBG)
        #if(DBG):print(world)
    (sleeper, most_slept_minute) = find_most_slept_minute(world)
    return (sleeper, most_slept_minute)



t1="""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""
tt1 = t1.splitlines()
(longest_sleeper, most_slept_minute) = process_schedule(tt1,True)
print(longest_sleeper, most_slept_minute)
print(int(longest_sleeper)* most_slept_minute)
#sys.exit()

INPUT_FILE="input-d04.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


(longest_sleeper, most_slept_minute) = process_schedule(puzzle_input,True)
print(longest_sleeper, most_slept_minute)
print(int(longest_sleeper)* most_slept_minute)

################# 56506 = 1487 * 38 too high
####### 1493 * 26 = 38818 too high
