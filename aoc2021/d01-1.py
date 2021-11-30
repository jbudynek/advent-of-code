# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from collections import deque
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
import pickle
import copy
import operator
import re
import string
import sys
import time
from timeit import default_timer as timer

import numpy as np


##########
######### HELPERS
###########

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
    if(DBG): print(xyids)
    x_min = min(coords, key = lambda t: t[0])[0]-1
    x_max = max(coords, key = lambda t: t[0])[0]+1
    y_min = min(coords, key = lambda t: t[1])[1]-1
    y_max = max(coords, key = lambda t: t[1])[1]+1
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    for yy in range(y_min,y_max+1):
        ss = ""
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids:
                ss += str(xyids[(xx,yy)])
            else:
                ss += " "
        print(ss)
    
    #delete_last_lines(y_max-y_min)

def print_tracks_and_vehicles(xyids, vehicles,vehicles_id_to_v_and_count, DBG=True):
    coords = xyids.keys()
    if(DBG): print(xyids)
    x_min = min(coords, key = lambda t: t[0])[0]-1
    x_max = max(coords, key = lambda t: t[0])[0]+1
    y_min = min(coords, key = lambda t: t[1])[1]-1
    y_max = max(coords, key = lambda t: t[1])[1]+1
    
    if(DBG): print(x_min,x_max,y_min,y_max)

    for yy in range(y_min,y_max+1):
        ss = ""
        for xx in range(x_min,x_max+1):
            if (xx,yy) in xyids:
                if (xx,yy) in vehicles:
                    v = vehicles_id_to_v_and_count[vehicles[(xx,yy)]][0]
                    ss += str(v)
                else:
                    ss += str(xyids[(xx,yy)])
            else:
                ss += " "
        print(ss)
    
    #delete_last_lines(y_max-y_min)



def create_world(ccc, DBG=True):
    field = {}
    vehicles = {}
    vehicles_id_to_v_and_count = {}
    x=-1
    y=-1
    v_id=0
    for line in ccc:
        y+=1
        x=-1
        for c in line:
            x+=1
            if c==' ' or c=='#': 
                continue
            elif c=='<' or c=='>': 
                field[(x,y)]='-'
                vehicles[(x,y)]=v_id
                vehicles_id_to_v_and_count[v_id] = (c,0)
                v_id = v_id+1
            elif c=='^' or c=='v': 
                field[(x,y)]='|'
                vehicles[(x,y)]=v_id
                vehicles_id_to_v_and_count[v_id] = (c,0)
                v_id = v_id+1
            else: 
                field[(x,y)]=c

    if DBG:print(field)
    if DBG:print_tracks_and_vehicles(field,vehicles,vehicles_id_to_v_and_count)
    
    return (field,vehicles,vehicles_id_to_v_and_count)


def strings_to_int_array(ii):
    ii = ii.split(",")
    ii = np.asarray(ii, dtype=int)
    #re.findall(r'\d+', 'hello 42 I\'m a 32 string 30')
    return ii

def get_bounds(tracks, DBG):
    coords = tracks.keys()
    x_min = min(coords, key = lambda t: t[0])[0]
    x_max = max(coords, key = lambda t: t[0])[0]
    y_min = min(coords, key = lambda t: t[1])[1]
    y_max = max(coords, key = lambda t: t[1])[1]
    return (x_min,x_max,y_min,y_max)

######## MAIN FUNCTION

def boom(input_val, DBG = True):
    ret=0
    for ii in input_val:
        ia = strings_to_int_array(ii)
        ret += np.sum(ia)
    return ret

#############
############
#############

def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

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


##########
################
########## TEST CASES
#########
###########

# tt1="1,2,3"
# test(tt1,6,True) 
# sys.exit()

t1="""92510
712
787"""
tt1 = t1.splitlines()
test(tt1,94009,True) 
#sys.exit()

#############
################
#############

######### parse all lines

INPUT_FILE = "input.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

##### treat each line differently
if(False):
    INPUT_FILE="input.txt"

    f = open(INPUT_FILE, "r")
    contents = f.read()
    puzzle_input = contents.splitlines()
    f.close()

    t_start = timer()

    nn = 0
    kk = 0
    for pp in puzzle_input:
        result = boom(pp,False)
        nn = nn + result
        kk = kk+1
        #if (kk==10):break

    t_end = timer()
    print_time(t_start, t_end)

    print(nn)
