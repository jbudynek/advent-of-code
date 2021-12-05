# coding: utf-8
from timeit import default_timer as timer

import numpy as np

# Helpers
##########

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

# Main function
##########

def parse_line(ll, DBG=True):
    ll = ll.split(" -> ")
    origin = np.asarray(ll[0] .split(","), dtype=int)
    dest = np.asarray(ll[1] .split(","), dtype=int)
    return (origin,dest)

def fill_world(w,o,d,DBG=True):
    # find director vector, and move from origin to destination
    vd = np.subtract(d,o)
    # only horizontal / vertical
    if (np.not_equal(vd,[0,0])).all():
        return
    vdn = np.sign(vd)
    cur = np.copy(o)
    while (np.not_equal(cur,d)).any():
        if not (cur[0],cur[1]) in w:
             w[(cur[0],cur[1])] = 0
        w[(cur[0],cur[1])] += 1
        cur = np.add(cur,vdn)
    # dont forget the last one
    if not (cur[0],cur[1]) in w:
            w[(cur[0],cur[1])] = 0
    w[(cur[0],cur[1])] += 1
    if DBG: print_field(w)
    return w


def boom(input_val, DBG=True):
    #w orld=dict of (xy)
    world = {}
    # loop on lines
    for ii in input_val:
        # parse line
        (origin, destination) = parse_line(ii,DBG)
        # fill matrix (horizontal/vertical only)
        fill_world(world,origin,destination,DBG)
    # iterate dict count where >1
    ret = 0
    for k,v in world.items():
        if v>1:
            ret +=1
    return ret

# Testing and timing
##########


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


# Test cases
##########

tt1 = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
tt1 = tt1.splitlines()
test(tt1, 5, True)
# sys.exit()

##########

INPUT_FILE = "input-d05.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# PART 1 OK = 3990
