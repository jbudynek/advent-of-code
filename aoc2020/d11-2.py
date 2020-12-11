# coding: utf-8
import copy
import re
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time

import numpy as np

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)


def print_field(xyids, DBG=True):

    coords = xyids.keys()
    if(DBG):
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0]-1
    x_max = max(coords, key=lambda t: t[0])[0]+1
    y_min = min(coords, key=lambda t: t[1])[1]-1
    y_max = max(coords, key=lambda t: t[1])[1]+1

    if(DBG):
        print(x_min, x_max, y_min, y_max)

    # delete_last_lines(y_max-y_min)

    for yy in range(y_min, y_max+1):
        ss = ""
        for xx in range(x_min, x_max+1):
            if (xx, yy) in xyids:
                ss += xyids[(xx, yy)]
            else:
                ss += " "
        print(ss)
#    time.sleep(0.3)


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
            else:
                field[(x, y)] = c

    if DBG:
        print(field)
    coords = field.keys()
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]
    return (field, x_min, x_max, y_min, y_max)


def count_in_dir(world, x_min, x_max, y_min, y_max, x, y, dx, dy, DBG):
    cur_x = x
    cur_y = y
    while (cur_x >= x_min) and (cur_x <= x_max) and (cur_y >= y_min) and (cur_y <= y_max):
        cur_x = cur_x+dx
        cur_y = cur_y+dy
        if (cur_x, cur_y) in world and world[(cur_x, cur_y)] == '#':
            return 1
        elif (cur_x, cur_y) in world and world[(cur_x, cur_y)] == 'L':
            return 0
    return 0


def count_occupied(world, x_min, x_max, y_min, y_max, x, y, DBG):
    occ = 0

    for (dx, dy) in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        occ = occ + count_in_dir(world, x_min, x_max,
                                 y_min, y_max, x, y, dx, dy, DBG)
    return occ


def tick(world, x_min, x_max, y_min, y_max, DBG=False):
    new_world = {}
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if (x, y) in world:
                occ = count_occupied(world, x_min, x_max,
                                     y_min, y_max, x, y, DBG)
                if world[(x, y)] == 'L':
                    if occ == 0:
                        new_world[(x, y)] = '#'
                    else:
                        new_world[(x, y)] = 'L'
                elif world[(x, y)] == '#':
                    if occ >= 5:
                        new_world[(x, y)] = 'L'
                    else:
                        new_world[(x, y)] = '#'
    return new_world


def nb_occupied_seats(world, x_min, x_max, y_min, y_max, DBG=False):
    count = 0
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if (x, y) in world and world[(x, y)] == '#':
                count = count + 1
    return count


def boom(input_val, DBG=True):
    (world, x_min, x_max, y_min, y_max) = create_world(input_val, DBG)

    while(True):
        count = nb_occupied_seats(world, x_min, x_max, y_min, y_max)
        new_world = tick(world, x_min, x_max, y_min, y_max)
        if DBG:
            print_field(new_world)
        # aa=input()
        new_count = nb_occupied_seats(new_world, x_min, x_max, y_min, y_max)
        if (new_count == count):
            break
        world = new_world

    return count


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


t1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
tt1 = t1.splitlines()
test(tt1, 26, True)
# sys.exit()

INPUT_FILE = "input-d11.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 1937
