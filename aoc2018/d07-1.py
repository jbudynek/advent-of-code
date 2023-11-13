# coding: utf-8

import time

import networkx as nx


def build_world(ii, DBG=True):
    world = nx.DiGraph()
    for line in ii:
        # "Step C must be finished before step A can begin"
        node_from = list(line)[5]
        node_to = list(line)[36]
        if DBG:
            print(node_from, node_to)
        world.add_node(node_from)
        world.add_node(node_to)
        world.add_edge(node_from, node_to)
    if DBG:
        print(world.edges)
    return world


def function(ii, DBG=True):

    # build world = build DAG
    # topological sort

    world = build_world(ii, DBG)

    ts = list(nx.lexicographical_topological_sort(world))

    if DBG:
        print(ts)

    return "".join(ts)


def test(cc=None, expected=None, DBG=False):

    start_millis = int(round(time.time() * 1000))

    result = str(function(cc, DBG))

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "*** " + str(cc) + " *** -> Result = " + str(result),
        " -> success = " + str(flag) + " -> expected " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


t1 = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
tt1 = t1.splitlines()
test(tt1, "CABDFE", True)  #

# sys.exit()

INPUT_FILE = "input-d07.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input, True)  #
print(ret)
