# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# from collections import defaultdict
# from collections import deque
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
from collections import Counter
import pickle
import copy
import operator
import re
import string
import sys
import time
from timeit import default_timer as timer

import numpy as np

# Helpers
##########

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'

RED_BG = '\x1b[101m'
GREEN_BG = '\x1b[102m'
YELLOW_BG = '\x1b[103m'
DEFAULT_BG = '\x1b[49m'


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
#        sys.stdout.write(CURSOR_UP_ONE)
#        sys.stdout.write(ERASE_LINE)


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

    for yy in range(y_min, y_max+1):
        ss = ""
        for xx in range(x_min, x_max+1):
            if (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)

    # delete_last_lines(y_max-y_min)


def print_tracks_and_vehicles(xyids, vehicles, vehicles_id_to_v_and_count, DBG=True):
    coords = xyids.keys()
    if(DBG):
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0]-1
    x_max = max(coords, key=lambda t: t[0])[0]+1
    y_min = min(coords, key=lambda t: t[1])[1]-1
    y_max = max(coords, key=lambda t: t[1])[1]+1

    if(DBG):
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max+1):
        ss = ""
        for xx in range(x_min, x_max+1):
            if (xx, yy) in xyids:
                if (xx, yy) in vehicles:
                    v = vehicles_id_to_v_and_count[vehicles[(xx, yy)]][0]
                    ss += str(v)
                else:
                    ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)

    # delete_last_lines(y_max-y_min)


def create_world(ccc, DBG=True):
    field = {}
    vehicles = {}
    vehicles_id_to_v_and_count = {}
    x = -1
    y = -1
    v_id = 0
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == ' ' or c == '#':
                continue
            elif c == '<' or c == '>':
                field[(x, y)] = '-'
                vehicles[(x, y)] = v_id
                vehicles_id_to_v_and_count[v_id] = (c, 0)
                v_id = v_id+1
            elif c == '^' or c == 'v':
                field[(x, y)] = '|'
                vehicles[(x, y)] = v_id
                vehicles_id_to_v_and_count[v_id] = (c, 0)
                v_id = v_id+1
            else:
                field[(x, y)] = c

    if DBG:
        print(field)
    if DBG:
        print_tracks_and_vehicles(field, vehicles, vehicles_id_to_v_and_count)

    return (field, vehicles, vehicles_id_to_v_and_count)


def count(ii, DBG):
    c = Counter(ii)
    if DBG:
        print(c)
    return c


def get_bounds(tracks, DBG):
    coords = tracks.keys()
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]
    return (x_min, x_max, y_min, y_max)


def strings_to_int_array(ii):
    ii = ii.split(",")
    ii = np.asarray(ii, dtype=int)
    #re.findall(r'\d+', 'hello 42 I\'m a 32 string 30')
    return ii

# Main function
##########


def boom_part1(input_val, DBG=True):
    # ugly way, by growing a list!
    ia = strings_to_int_array(input_val[0])

    nb_z = 0
    for day in np.arange(1, 81):
        ia = ia - 1
        ia[ia == -1] = 6
        ia = np.append(ia, [8]*nb_z)
        nb_z = np.count_nonzero(ia == 0)
        if DBG:
            lenia = len(ia)
            print(day, lenia, ia)

    return len(ia)


def boom_part2(input_val, DBG=True):
    # ok way, by counting the right things and not worrying about the list.
    ia = np.asarray(input_val[0].split(","), dtype=int)

    status_to_count = np.zeros(9, dtype=int)

    for i in ia:
        status_to_count[i] += 1
    nb_z = 0
    for day in np.arange(1, 257):
        loopy = status_to_count[0]
        for i in range(1, 9):
            status_to_count[i-1] = status_to_count[i]
        status_to_count[6] += loopy
        status_to_count[8] = nb_z
        nb_z = status_to_count[0]
        if DBG:
            print(day, status_to_count)

    return np.sum(status_to_count)

# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)

# Test cases
##########


tt1 = "3,4,3,1,2"
tt1 = tt1.splitlines()
test_part1(tt1, 5934, True)
test_part2(tt1, 26984457539, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d06.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 386536
# PART 2 OK = 1732821262171
