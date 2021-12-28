# coding: utf-8
import sys
import copy
import time
from timeit import default_timer as timer

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


def delete_last_lines_xmas(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE  + CURSOR_UP_ONE)


def print_field_xmas(xyids):
    coords = xyids.keys()
    (x_min, x_max, y_min, y_max)=(0,140,0,140)
    delete_last_lines_xmas(y_max-y_min+2)

    for yy in range(y_min, y_max+1):
        ss = ""
        for xx in range(x_min, x_max+1):
            if (xx, yy) in xyids:
                if xyids[(xx, yy)]=='>':
                    ss += GREEN_FG+'>'+DEFAULT_FG
                else:
                    ss += RED_FG+'V'+DEFAULT_FG
            else:
                ss += " "
        print(ss)
    #time.sleep(0.01)

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

def create_world(ccc, DBG=True):
    width = len(ccc[0])
    height = len(ccc)
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c != '.':
                field[(x, y)] = c

    if DBG:
        print(field)

    return field, width, height

# Main function
##########


def move_east(world, width, height):
    new_world = {}
    for k in world.keys():
        if world[k] == '>':
            nxy = ((k[0]+1) % width, k[1])
            if nxy not in world:
                new_world[nxy] = '>'
            else:
                new_world[k] = '>'
        elif world[k] == 'v':
            new_world[k] = 'v'
    return new_world


def move_south(world, width, height):
    new_world = {}
    for k in world.keys():
        if world[k] == 'v':
            nxy = (k[0], (k[1]+1) % height)
            if nxy not in world:
                new_world[nxy] = 'v'
            else:
                new_world[k] = 'v'
        elif world[k] == '>':
            new_world[k] = '>'
    return new_world


def boom_part1(input_val, DBG=True):

    # parse world
    world, width, height = create_world(input_val, DBG)
    # step =0
    step = 0
    if DBG:
        print_field(world, DBG)
        print("step ",step)
    # loop
    while True:
        # step +=1
        step += 1
        # copy current state
        latest_state = copy.deepcopy(world)
        # try to move east and move east
        world = move_east(world, width, height)
        # try to move south and move south
        world = move_south(world, width, height)
        # if state is the same, we're done
        print_field_xmas(world) # for seasonal animaltion
        if DBG:
            print_field(world, DBG)
            print("step ",step)
        if world == latest_state:
            return step
        # else start again


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

# Test cases
##########


tt1 = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
tt1 = tt1.splitlines()
test_part1(tt1, 58, False)
#sys.exit()
##########

INPUT_FILE = "input-d25.txt"
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

# PART 1 OK = 489
