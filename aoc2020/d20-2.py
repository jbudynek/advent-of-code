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
import pickle
import re
import string
import sys
import time
from itertools import permutations, product
from timeit import default_timer as timer

import numpy as np

# general idea: build big picture based on part one results
# rotate and flip it until some snakes are found inside!


def rotate_tile_w(tile, w):
    ret = np.zeros((w, w), dtype=np.int)
    for x in range(w):
        for y in range(w):
            ret[x, y] = tile[w-1-y, x]
    return ret


def flip_tile_h_w(tile, w):
    ret = np.zeros((w, w), dtype=np.int)
    for x in range(w):
        for y in range(w):
            ret[x, y] = tile[x, w-1-y]
    return ret


def print_tiles(tiles):
    ss = ""
    for (id, tile) in tiles.items():
        ss = ss + str(id)+"\n"
        for x in range(10):
            for y in range(10):
                if tile[x, y] == 1:
                    ss = ss+"#"
                elif tile[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        ss = ss + "\n"
    print(ss)


def parse_tiles(input_val, DBG):
    tiles = {}
    tile = np.zeros((10, 10), dtype=np.int)
    tile_id = 0
    x = 0
    for ii in input_val:

        if ii == '':
            tiles[tile_id] = tile
            tile = np.zeros((10, 10), dtype=np.int)
            x = 0
        elif ii.startswith('Tile'):
            tile_id = np.asarray(re.findall(r'\d+', ii), dtype=np.int)[0]
        else:
            y = 0
            for c in ii:
                if c == '.':
                    tile[x, y] = 0
                elif c == '#':
                    tile[x, y] = 1
                else:
                    sys.exit("panic"+ii)
                y = y+1
            x = x+1

    if not tile_id in tiles:
        tiles[tile_id] = tile

    if DBG:
        print(tiles)
        print_tiles(tiles)
    return tiles


def applyops_w(ops, tile, w):
    r_op = ops[0]  # ["r0", "r1", "r2", "r3"]
    f_op = ops[1]  # ["i", "h"]
    ret = np.copy(tile)
    if (r_op == "r0"):
        pass
    elif (r_op == "r1"):
        ret = rotate_tile_w(ret, w)
    elif (r_op == "r2"):
        ret = rotate_tile_w(ret, w)
        ret = rotate_tile_w(ret, w)
    elif (r_op == "r3"):
        ret = rotate_tile_w(ret, w)
        ret = rotate_tile_w(ret, w)
        ret = rotate_tile_w(ret, w)

    if (f_op == "i"):
        pass
    elif (f_op == "h"):
        ret = flip_tile_h_w(ret, w)
    return ret


def boom(input_val, DBG=True):
    tiles = parse_tiles(input_val, DBG)

    nb_tiles = len(tiles)
    ww = int(np.sqrt(nb_tiles))
    if DBG:
        print(ww)

    # load results from part one
    sorted_ids = load_obj("sorted_ids_"+str(ww))
    placed_tiles = load_obj("placed_tiles"+str(ww))
    placed_tiles_id = load_obj("placed_tiles_id"+str(ww))
    inv_ptid = {v: k for k, v in placed_tiles_id.items()}

    if DBG:
        print(placed_tiles)
    if DBG:
        print(sorted_ids)
    if DBG:
        print(placed_tiles_id)
    if DBG:
        print(inv_ptid)

    # build the bigger picture
    big_pic = np.zeros((8*ww, 8*ww), dtype=np.int)

    idx = 0
    for ii in sorted_ids:
        xx = idx//ww
        yy = idx % ww
        tile = placed_tiles[inv_ptid[ii]]
        big_pic[(xx)*8:(xx+1)*8, (yy)*8:(yy+1)*8] = tile[1:9, 1:9]
        idx = idx + 1

    if DBG:
        print(big_pic)

    # build the snake
    snake = np.zeros((3, 20), dtype=np.int)
    snake[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    snake[1] = [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1]
    snake[2] = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

    if DBG:
        print(snake)
    #     """
    #                   #
    # #    ##    ##    ###
    #  #  #  #  #  #  #
    #  """

    big_pic_0 = np.copy(big_pic)

    count_rough_0 = np.sum(big_pic_0)
    ret = count_rough_0

    # try all geom transformations, find the one where we have some matches, and return the count

    r_op = ["r0", "r1", "r2", "r3"]
    f_op = ["i", "h"]  # , v is not needed as (r2 and h) = v
    all_ops = list(product(r_op, f_op))

    for op in all_ops:
        big_pic = np.copy(big_pic_0)
        big_pic = applyops_w(op, big_pic, 8*ww)
        if DBG:
            print("***")
            print(op)
            print(big_pic_0)
            print(big_pic)

        # match snakes
        for x in range(8*ww-3):
            for y in range(8*ww-20):
                big_pic = test_snake(big_pic, snake, x, y)

        ret = np.sum(big_pic)
        if not ret == count_rough_0:
            break

    return ret


def test_snake(big_pic, snake, x, y):

    match = True
    for xx in range(3):
        for yy in range(20):
            if (snake[xx, yy] == 1) and not (big_pic[x+xx, y+yy] == 1):
                match = False
                break

    if(match):
        for xx in range(3):
            for yy in range(20):
                if (snake[xx, yy] == 1):
                    big_pic[x+xx, y+yy] = 0
    return big_pic


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


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


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


t1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""


tt1 = t1.splitlines()
test(tt1, 273, True)
# sys.exit()

INPUT_FILE = "input-d20.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 2 = 1841
