# coding: utf-8
import networkx as nx
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


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            field[(x, y)] = int(c)

    if DBG:
        print(field)

    return field


def create_network(field, DBG=True):
    G = nx.Graph()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for xy in field.keys():
        G.add_node(xy, weight=field[xy])
    for xy in field.keys():
        for d in dirs:
            nxy = (xy[0]+d[0], xy[1]+d[1])
            if nxy in field:
                G.add_edge(xy, nxy)
    if DBG:
        print(G.nodes, G.edges)
    return G


# Main function
##########

def boom_part1(input_val, DBG=True):

    world = create_world(input_val, False)

    GG = create_network(world, False)

    source = (0, 0)
    dest = int(np.sqrt(len(world.keys())))
    target = (dest-1, dest-1)

    def func(u, v, d):
        node_u_wt = GG.nodes[u].get("weight", 1)
        node_v_wt = GG.nodes[v].get("weight", 1)
        return node_u_wt + node_v_wt

    path = nx.dijkstra_path(GG, source, target, weight=func)

    ret = 0
    for n in path:
        ret += GG.nodes[n].get("weight")
    ret -= GG.nodes[source].get("weight")

    return ret


def increase(n, delta):
    ret = ((n-1 + delta) % 9) + 1
    return ret


def multiply_world(small_world, nb):

    world = small_world.copy()
    size = int(np.sqrt(len(small_world.keys())))
    for xy in small_world.keys():
        for i in range(0, nb):
            for j in range(0, nb):
                nx = xy[0] + size*i
                ny = xy[1] + size*j
                world[(nx, ny)] = increase(small_world[xy], i+j)
    return world


def boom_part2(input_val, DBG=True):

    small_world = create_world(input_val, False)

    world = multiply_world(small_world, 5)
    if DBG:
        print_field(world)

    GG = create_network(world, False)

    source = (0, 0)
    dest = int(np.sqrt(len(world.keys())))
    target = (dest-1, dest-1)

    def func(u, v, d):
        node_u_wt = GG.nodes[u].get("weight", 1)
        node_v_wt = GG.nodes[v].get("weight", 1)
        return node_u_wt + node_v_wt

    path = nx.dijkstra_path(GG, source, target, weight=func)

    ret = 0
    for n in path:
        ret += GG.nodes[n].get("weight")
    ret -= GG.nodes[source].get("weight")

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


tt1 = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
tt1 = tt1.splitlines()
test_part1(tt1, 40, True)
test_part2(tt1, 315, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d15.txt"
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

# PART 1 OK = 429
# PART 2 OK = 2844
