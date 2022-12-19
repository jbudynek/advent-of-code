# coding: utf-8
import re

import networkx as nx
from boilerplate import read_input_file, run_func, test_func

# import sys


def make_world(input_val):
    cubes = {}
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    minz = 0
    maxz = 0
    for line in input_val:
        xyz = list(map(int, re.findall(r"-?\d+", line)))
        maxx = max(xyz[0], maxx)
        minx = min(xyz[0], minx)
        maxy = max(xyz[1], maxy)
        miny = min(xyz[1], miny)
        maxz = max(xyz[2], maxz)
        minz = min(xyz[2], minz)

        cubes[tuple(xyz)] = 1
    return cubes, minx, maxx, miny, maxy, minz, maxz


def get_sides(cubes):
    # check points in the middle of sides
    all_sides = set()
    d_s = [
        (0.5, 0, 0),
        (-0.5, 0, 0),
        (0, 0.5, 0),
        (0, -0.5, 0),
        (0, 0, 0.5),
        (0, 0, -0.5),
    ]
    for cube in cubes.keys():
        for d in d_s:
            side = (cube[0] + d[0], cube[1] + d[1], cube[2] + d[2])
            all_sides = all_sides ^ set([side])
    return all_sides


def boom_part1(input_val, DBG=True):

    cubes, _, _, _, _, _, _ = make_world(input_val)

    all_sides = get_sides(cubes)

    return len(all_sides)


def boom_part2(input_val, DBG=True):
    cubes, minx, maxx, miny, maxy, minz, maxz = make_world(input_val)
    G = nx.Graph()
    for x in range(minx - 1, maxx + 2):
        for y in range(miny - 1, maxy + 2):
            for z in range(minz - 1, maxz + 2):
                xyz = (x, y, z)
                if xyz not in cubes:
                    G.add_node(xyz)
                    d_c = [
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ]
                    for d in d_c:
                        xyz2 = (x + d[0], y + d[1], z + d[2])
                        if xyz2 not in cubes:
                            G.add_node(xyz2)
                            G.add_edge(xyz, xyz2)

    # get all connected components
    # and subtract their size from the raw side count
    # the biggest component is "around" so we don't count its size

    ccs = nx.connected_components(G)
    all_cc_sizes = []
    for cc in ccs:
        ff = {}
        for n in cc:
            ff[n] = 1
        sides = get_sides(ff)
        all_cc_sizes.append(len(sides))

    all_sides = len(get_sides(cubes))
    all_cc_sizes = sorted(all_cc_sizes)

    return all_sides - sum(all_cc_sizes[:-1])


# Test cases
##########


t1 = """1,1,1
2,1,1"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 10, True)

t1 = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 64, True)
test_func(boom_part2, tt1, 58, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d18.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 4370
# PART 2 OK = 2458
