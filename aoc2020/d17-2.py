# coding: utf-8
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
# from functools import reduce
# from math import log
import copy
import operator
import re
import sys
import time
from itertools import product

import numpy as np

# ok for dimension 4 let's use a dict indexed by (x,y,z,w) - that idea would have worked with dimension 3 also.


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == '.':
                continue
            elif c == '#':
                field[(x, y, 0, 0)] = c
            else:
                print("panic")
                sys.exit()
    return field


def get_world_bounds(world):
    w_min = 0
    w_max = 0
    z_min = 0
    z_max = 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    coords = world.keys()
    x_min = min(x_min, min(coords, key=lambda t: t[0])[0])
    x_max = max(x_max, max(coords, key=lambda t: t[0])[0])
    y_min = min(y_min, min(coords, key=lambda t: t[1])[1])
    y_max = max(y_max, max(coords, key=lambda t: t[1])[1])
    z_min = min(z_min, min(coords, key=lambda t: t[2])[2])
    z_max = max(z_max, max(coords, key=lambda t: t[2])[2])
    w_min = min(w_min, min(coords, key=lambda t: t[3])[3])
    w_max = max(w_max, max(coords, key=lambda t: t[3])[3])

    return (x_min, x_max, y_min, y_max, z_min, z_max, w_min, w_max)


def is_active(world, x, y, z, w):
    return (x, y, z, w) in world


def set_active(new_world, x, y, z, w):
    if not (x, y, z, w) in new_world:
        new_world[(x, y, z, w)] = '#'


def set_inactive(new_world, x, y, z, w):
    if (x, y, z, w) in new_world:
        del new_world[(x, y, z, w)]


def neighbors(world, x, y, z, w):
    n = 0
    for (dx, dy, dz, dw) in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
        if (dx, dy, dz, dw) == (0, 0, 0, 0):
            continue
        if (x+dx, y+dy, z+dz, w+dw) in world:
            n = n + 1
    return n


def count_cubes(world):
    ret = len(world.values())
    return ret


def tick(world, x_min, x_max, y_min, y_max, z_min, z_max, w_min, w_max, DBG=True):
    new_world = {}
    for w in range(w_min-1, w_max+2):
        for z in range(z_min-1, z_max+2):
            for y in range(y_min-1, y_max+2):
                for x in range(x_min-1, x_max+2):
                    n = neighbors(world, x, y, z, w)
                    a = is_active(world, x, y, z, w)
                    if a:
                        if (n == 2 or n == 3):
                            set_active(new_world, x, y, z, w)
                        else:
                            set_inactive(new_world, x, y, z, w)
                    elif not a:
                        if n == 3:
                            set_active(new_world, x, y, z, w)
                        else:
                            set_inactive(new_world, x, y, z, w)

    (x_min, x_max, y_min, y_max, z_min, z_max,
     w_min, w_max) = get_world_bounds(new_world)
    return (new_world, x_min, x_max, y_min, y_max, z_min, z_max, w_min, w_max)


def boom(input_val, DBG=True):

    # parse world
    world = create_world(input_val, DBG)

    (x_min, x_max, y_min, y_max, z_min, z_max,
     w_min, w_max) = get_world_bounds(world)

    max_tick = 6

    t = 0
    if DBG:
        print("tick=", t)

    count = 0

    while(True):
        t = t+1
        (new_world, new_x_min, new_x_max, new_y_min, new_y_max, new_z_min,
         new_z_max, new_w_min, new_w_max) = tick(world, x_min, x_max, y_min, y_max, z_min, z_max, w_min, w_max, DBG)
        world = new_world
        x_min = new_x_min
        x_max = new_x_max
        y_min = new_y_min
        y_max = new_y_max
        z_min = new_z_min
        z_max = new_z_max
        w_min = new_w_min
        w_max = new_w_max

        count_new = count_cubes(world)

        if DBG:
            print("tick=", t, "count=", count_new)

        if (count_new == count):
            print("***TICK", t, "***", count_new, "stable")
            break

        count = count_new
        if t == max_tick:
            if DBG:
                print("***TICK", t, "***", count_new)
            break

    ret = count

    return ret


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + str(flag) + " -> expected " + expected)
    print((stop_millis-start_millis), "ms", int((stop_millis-start_millis) /
                                                1000), "s", int((stop_millis-start_millis)/1000/60), "min")
    return flag


t1 = """.#.
..#
###"""
tt1 = t1.splitlines()
test(tt1, 848, True)
# sys.exit()

INPUT_FILE = "input-d17.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 2028
