# coding: utf-8
import itertools
from timeit import default_timer as timer

import networkx as nx

# Main function
##########


def build_net(input_val, DBG=True):
    net = nx.Graph()
    for line in input_val:
        ll = line.split()
        if DBG:
            print(ll)
        net.add_edge(ll[0], ll[2], weight=int(ll[4]))
    return net


def find_path_length(net, init, func, DBG=True):
    mw = init
    for p in list(itertools.permutations(net.nodes)):
        w = nx.path_weight(net, p, "weight")
        mw = func(w, mw)
        if DBG:
            print(w)
    return mw


def boom_part1(input_val, DBG=True):
    net = build_net(input_val, DBG)
    mw = find_path_length(net, 10000, min, DBG)
    return mw


def boom_part2(input_val, DBG=True):
    net = build_net(input_val, DBG)
    mw = find_path_length(net, 0, max, DBG)
    return mw


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
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


tt1 = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 605, True)
test_part2(tt1, 982, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d09.txt"
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

# PART 1 OK = 141
# PART 2 OK = 736
