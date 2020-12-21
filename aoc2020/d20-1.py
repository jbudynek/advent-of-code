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
import string
import sys
import time
import pickle
from itertools import permutations, product
from timeit import default_timer as timer

import numpy as np

# general idea: solve it like a real life jigsaw puzzle:
# put down first tile, then try to find which one matches on each sides
# performance seems suboptimal (~35 seconds on my computer)
# (note: saves results for part two)


def rotate_tile(tile):
    ret = np.zeros((10, 10), dtype=np.int)
    for x in range(10):
        for y in range(10):
            ret[x, y] = tile[9-y, x]
    return ret


def flip_tile_h(tile):
    ret = np.zeros((10, 10), dtype=np.int)
    for x in range(10):
        for y in range(10):
            ret[x, y] = tile[x, 9-y]
    return ret


def get_match(tile1, tile2):
    if (tile1[0, :] == tile2[9, :]).all():
        return "N"
    elif (tile2[0, :] == tile1[9, :]).all():
        return "S"
    elif (tile2[:, 0] == tile1[:, 9]).all():
        return "E"
    elif (tile2[:, 9] == tile1[:, 0]).all():
        return "W"
    else:
        return "X"


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


def unit_tests(tiles):
    t1 = tiles[3079]
    t2 = rotate_tile(t1)
    test = {}
    test["t1"] = t1
    test["t2"] = t2
    print_tiles(test)
    print(get_match(t1, t2))

    t1 = tiles[3079]
    t2 = flip_tile_h(t1)
    test = {}
    test["t1"] = t1
    test["t2"] = t2
    print_tiles(test)
    print(get_match(t1, t2))


def applyops(ops, tile):
    r_op = ops[0]  # ["r0", "r1", "r2", "r3"]
    f_op = ops[1]  # ["i", "h"]
    ret = np.copy(tile)
    if (r_op == "r0"):
        pass
    elif (r_op == "r1"):
        ret = rotate_tile(ret)
    elif (r_op == "r2"):
        ret = rotate_tile(ret)
        ret = rotate_tile(ret)
    elif (r_op == "r3"):
        ret = rotate_tile(ret)
        ret = rotate_tile(ret)
        ret = rotate_tile(ret)

    if (f_op == "i"):
        pass
    elif (f_op == "h"):
        ret = flip_tile_h(ret)
    return ret


def print_two_tiles(m, t1, t2):
    if (m == 'N'):
        ss = ""
        for x in range(10):
            for y in range(10):
                if t2[x, y] == 1:
                    ss = ss+"#"
                elif t2[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        ss = ss + "NNNNNNNNNN\n"
        for x in range(10):
            for y in range(10):
                if t1[x, y] == 1:
                    ss = ss+"#"
                elif t1[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        print(ss)
        return ss

    if (m == 'S'):
        ss = ""
        for x in range(10):
            for y in range(10):
                if t1[x, y] == 1:
                    ss = ss+"#"
                elif t1[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        ss = ss + "SSSSSSSSSS\n"
        for x in range(10):
            for y in range(10):
                if t2[x, y] == 1:
                    ss = ss+"#"
                elif t2[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        print(ss)
        return ss

    if (m == 'E'):
        ss = ""
        for x in range(10):
            for y in range(10):
                if t1[x, y] == 1:
                    ss = ss+"#"
                elif t1[x, y] == 0:
                    ss = ss+"."
            ss = ss + "E"
            for y in range(10):
                if t2[x, y] == 1:
                    ss = ss+"#"
                elif t2[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        print(ss)
        return ss

    if (m == 'W'):
        ss = ""
        for x in range(10):
            for y in range(10):
                if t2[x, y] == 1:
                    ss = ss+"#"
                elif t2[x, y] == 0:
                    ss = ss+"."
            ss = ss + "W"
            for y in range(10):
                if t1[x, y] == 1:
                    ss = ss+"#"
                elif t1[x, y] == 0:
                    ss = ss+"."
            ss = ss + "\n"
        print(ss)
        return ss


def boom(input_val, DBG=True):
    tiles = parse_tiles(input_val, DBG)

    if DBG:
        unit_tests(tiles)

    nb_tiles = len(tiles)
    ww = int(np.sqrt(nb_tiles))
    if DBG:
        print(ww)
    if DBG:
        print("corners", 0, ww-1, ww*ww-ww, ww*ww-1)

    # rotate 0,1,2,3
    # flip h

    keys = tiles.keys()
    r_op = ["r0", "r1", "r2", "r3"]
    f_op = ["i", "h"]  # v is not needed as (r2 and h) = v
    all_ops = list(product(r_op, f_op))
    if DBG:
        print(len(all_ops), all_ops)

    # first tile does not move. try to put tiles on all four sides.
    # then, move to next tile

    available_tiles_id = list(keys).copy()

    placed_tiles_id = {}
    placed_tiles = {}

    # put first tile, start with last (for fun)
    start = -1
    t_id = available_tiles_id[start]
    available_tiles_id = np.delete(available_tiles_id, start)

    placed_tiles_id[0] = t_id
    placed_tiles[0] = np.copy(tiles[t_id])

    available_idx = 0

    while len(available_tiles_id) > 0:
        # get next available tile
        t1_id = available_tiles_id[available_idx]
        # try to put it next to every already placed tile
        # this NSEW business is rather ugly and error prone due to code duplication
        placed = False
        for placed_key in placed_tiles.keys():
            t0 = placed_tiles[placed_key]
            for op in all_ops:
                t1 = tiles[t1_id]
                t1_o = applyops(op, t1)
                if DBG:
                    print(t0, t1_o)
                m = get_match(t0, t1_o)
                if DBG:
                    print(op, m)
                if m == 'N':
                    if (placed_key-ww) in placed_tiles_id:
                        print("already!!")
                    placed_tiles_id[placed_key-ww] = t1_id
                    placed_tiles[placed_key-ww] = np.copy(t1_o)
                    available_tiles_id = np.delete(
                        available_tiles_id, available_idx)
                    if DBG:
                        print_two_tiles(m, t0, t1_o)
                    if DBG:
                        print(len(available_tiles_id))
                    placed = True
                    break
                elif m == 'S':
                    if (placed_key+ww) in placed_tiles_id:
                        print("already!!")
                    placed_tiles_id[placed_key+ww] = t1_id
                    placed_tiles[placed_key+ww] = np.copy(t1_o)
                    available_tiles_id = np.delete(
                        available_tiles_id, available_idx)
                    if DBG:
                        print_two_tiles(m, t0, t1_o)
                    if DBG:
                        print(len(available_tiles_id))
                    placed = True
                    break
                elif m == 'W':
                    if (placed_key-1) in placed_tiles_id:
                        print("already!!")
                    placed_tiles_id[placed_key-1] = t1_id
                    placed_tiles[placed_key-1] = np.copy(t1_o)
                    available_tiles_id = np.delete(
                        available_tiles_id, available_idx)
                    if DBG:
                        print_two_tiles(m, t0, t1_o)
                    if DBG:
                        print(len(available_tiles_id))
                    placed = True
                    break
                elif m == 'E':
                    if (placed_key+1) in placed_tiles_id:
                        print("already!!")
                    placed_tiles_id[placed_key+1] = t1_id
                    placed_tiles[placed_key+1] = np.copy(t1_o)
                    available_tiles_id = np.delete(
                        available_tiles_id, available_idx)
                    if DBG:
                        print_two_tiles(m, t0, t1_o)
                    if DBG:
                        print(len(available_tiles_id))
                    placed = True
                    break
                else:  # no match try next
                    pass
            if placed:
                break
        if placed:
            available_idx = 0
        else:
            available_idx = (available_idx + 1) % (len(available_tiles_id))
    if DBG:
        print(placed_tiles_id)
    if DBG:
        print(placed_tiles)
    if DBG:
        print_tiles(placed_tiles)

    sorted_ids = [placed_tiles_id[key]
                  for key in sorted(placed_tiles_id.keys())]

    if DBG:
        print(sorted_ids)
    p = sorted_ids

    ret = p[0]*p[ww-1]*p[ww*ww-ww]*p[ww*ww-1]

    if DBG:
        print(ret)

    save_obj(sorted_ids, "sorted_ids_"+str(ww))
    save_obj(placed_tiles, "placed_tiles"+str(ww))
    save_obj(placed_tiles_id, "placed_tiles_id"+str(ww))

    return ret


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


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
test(tt1, 20899048083289, True)
# sys.exit()

INPUT_FILE = "input-d20.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()
ret = boom(puzzle_input, DBG=False)
t_end = timer()
s = t_end-t_start
print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")

print(ret)

# part 1 = 8425574315321
