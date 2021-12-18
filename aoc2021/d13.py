# coding: utf-8
from collections import Counter
from timeit import default_timer as timer


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


def create_world(ccc, DBG=True):
    field = {}
    for l in ccc:
        xy = l.split(",")
        x = int(xy[0])
        y = int(xy[1])
        field[(x, y)] = '#'

    if DBG:
        print(field)

    return field

# Main function
##########


def add_fold(folds, l):
    f = l.split()[2].split('=')
    folds.append((f[0], int(f[1])))


def process_folds(world, folds, all, DBG):

    for fold in folds:
        l = fold[1]
        if fold[0] == 'x':
            for xy in list(world.keys()):
                x = xy[0]
                y = xy[1]
                if x > l:
                    del world[xy]
                    world[(l-(x-l), y)] = '#'
        elif fold[0] == 'y':
            for xy in list(world.keys()):
                x = xy[0]
                y = xy[1]
                if y > l:
                    del world[xy]
                    world[(x, l-(y-l))] = '#'

        if DBG:
            print_field(world)
        if not all:
            return

    return


def count_dots(world):
    return Counter(world.values())['#']  # size would also work


def parse_input(input_val, DBG):
    lines = []
    folds = []
    for l in input_val:
        if l == '':
            continue
        elif l[0] == "f":
            add_fold(folds, l)
        else:
            lines.append(l)

    world = create_world(lines, DBG)
    return (world, folds)


def boom_part1(input_val, DBG=True):

    (world, folds) = parse_input(input_val, DBG)

    process_folds(world, folds, False, DBG)

    if DBG:
        print_field(world, DBG)

    ret = count_dots(world)

    return ret


def boom_part2(input_val, DBG=True):
    (world, folds) = parse_input(input_val, DBG)

    process_folds(world, folds, True, DBG)

    print_field(world, DBG)

    ret = count_dots(world)

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


tt1 = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
tt1 = tt1.splitlines()
test_part1(tt1, 17, False)
test_part2(tt1, -1, False)

# Real data
##########

INPUT_FILE = "input-d13.txt"
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

# PART 1 OK = 631
# PART 2 OK = EFLFJGRF
