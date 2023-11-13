# coding: utf-8

import time

import networkx as nx

node_to_metadata = {}


def parse_node(idx, iii, tree, cur_node, DBG=True):
    this_node_name = cur_node
    cur_node = chr(ord(cur_node) + 1)
    tree.add_node(this_node_name)
    nb_children = iii[idx]
    idx = idx + 1
    nb_metadata = iii[idx]
    idx = idx + 1
    for k in range(nb_children):
        (node, idx, cur_node) = parse_node(idx, iii, tree, cur_node, DBG)
        tree.add_edge(this_node_name, node)
    metadata = []
    for k in range(nb_metadata):
        metadata.append(iii[idx])
        idx = idx + 1
    node_to_metadata[this_node_name] = metadata.copy()
    return (this_node_name, idx, cur_node)


def get_value(node, tree, DBG=True):
    children = list(tree.successors(node))
    if len(children) == 0:
        total_metadata = 0
        mm = node_to_metadata[node]
        for i in mm:
            total_metadata = total_metadata + i
        return total_metadata
    else:
        total_metadata = 0
        mm = node_to_metadata[node]
        for i in mm:
            if (i - 1) < len(children):
                total_metadata = total_metadata + get_value(children[i - 1], tree, DBG)
        return total_metadata


def function(ii, DBG=True):

    ss = ii.split()

    iii = [int(ns) for ns in ss]

    if DBG:
        print(iii)

    idx = 0
    tree = nx.DiGraph()
    cur_node = "A"
    (root, idx, cur_node) = parse_node(idx, iii, tree, cur_node, DBG)
    if DBG:
        print(str(tree.edges))

    ret = get_value(root, tree, DBG)

    return ret


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


t1 = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
# tt1 = t1.splitlines()
# test(t1,66,True) #

# sys.exit()

INPUT_FILE = "input-d08.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
# puzzle_input = contents.splitlines()
puzzle_input = contents.rstrip()
f.close()

ret = function(puzzle_input, True)  #
print(ret)
