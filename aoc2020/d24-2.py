# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
# from collections import deque
import copy
import operator
import re
import string
import sys
import time
from enum import Enum
from timeit import default_timer as timer

import numpy as np


class Dir(Enum):
    e = 0
    se = 1
    sw = 2
    w = 3
    nw = 4
    ne = 5


DELTA = {Dir.e: complex(2, 0), Dir.se: complex(1, -1), Dir.sw: complex(-1, -1),
         Dir.w: complex(-2, 0), Dir.nw: complex(-1, 1), Dir.ne: complex(1, 1)}

# black = 1
# white = 0


def parse_lines(input_val, DBG):
    lines = []

    for d in input_val:
        if d == "":
            continue
        line = []
        idx = 0
        while idx < len(d):
            if d[idx] == "e" or d[idx] == "w":
                dd = d[idx]
                line.append(Dir[dd])
                idx = idx + 1
            else:
                dd = Dir[d[idx]+d[idx+1]]
                line.append(dd)
                idx = idx + 2
        lines.append(line)

    if DBG:
        print(lines)

    return lines


def follow_one_line(line, DBG):
    z = complex(0, 0)
    for d in line:
        z = z + DELTA[Dir(d)]
    if DBG:
        print("tile in", z)
    return z


def follow_lines(lines, DBG=True):
    flipped_tiles = {}
    for line in lines:
        tile_to_flip = follow_one_line(line, DBG)
        if not tile_to_flip in flipped_tiles:
            flipped_tiles[tile_to_flip] = 0
        flipped_tiles[tile_to_flip] = (flipped_tiles[tile_to_flip]+1) % 2
        if DBG:
            print("tile in", tile_to_flip, "=", flipped_tiles[tile_to_flip])
    return flipped_tiles


def is_black_tile(zz, flipped_tiles):
    if zz in flipped_tiles and flipped_tiles[zz] == 1:
        return True
    else:
        return False


def is_white_tile(zz, flipped_tiles):
    return not is_black_tile(zz, flipped_tiles)


def nb_black_tiles_adjacent(zz, flipped_tiles):
    ret = 0
    for d in DELTA.values():
        ib = is_black_tile(zz+d, flipped_tiles)
        if ib:
            ret = ret + 1
    return ret


def tick(flipped_tiles, DBG):
    new_flipped_tiles = {}

    for tile in flipped_tiles:
        # deal with neighbors
        for d in DELTA.values():
            zz = tile + d
            nbta = nb_black_tiles_adjacent(zz, flipped_tiles)
            if is_black_tile(zz, flipped_tiles) and (nbta == 0 or nbta > 2):
                pass
            elif is_white_tile(zz, flipped_tiles) and (nbta == 2):
                new_flipped_tiles[zz] = 1

        # then deal with this tile
        nbta = nb_black_tiles_adjacent(tile, flipped_tiles)
        if is_black_tile(tile, flipped_tiles) and (nbta == 0 or nbta > 2):
            pass
        elif is_white_tile(tile, flipped_tiles) and (nbta == 2):
            new_flipped_tiles[tile] = 1
        elif tile in flipped_tiles and flipped_tiles[tile] == 1:
            new_flipped_tiles[tile] = flipped_tiles[tile]

    return new_flipped_tiles

################


def boom(input_val, DBG=True):
    lines = parse_lines(input_val, DBG)

    # initial state
    flipped_tiles = follow_lines(lines, DBG)

    # tick
    max_tick = 100
    for cur_tick in range(1, max_tick+1):
        flipped_tiles = tick(flipped_tiles, DBG)
        number_black = sum(flipped_tiles.values())
        if DBG:
            print("Day", cur_tick, ":", number_black)

    return number_black

########################


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
#######


t1 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

tt1 = t1.splitlines()
test(tt1, 2208, True)
# sys.exit()

#########

INPUT_FILE = "input-d24.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 2 = 4135
