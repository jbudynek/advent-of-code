# coding: utf-8

import networkx as nx
import numpy as np
from boilerplate import read_input_file, run_func, test_func

# Main function
################


def create_graph(input_val, DBG=True):
    G = nx.DiGraph()
    for line in input_val:
        nodes = line.split(" ")
        G.add_node(nodes[0], weight=int(nodes[1][1:-1]))  # ADD WEIGHT
        l_nodes = len(nodes)
        if l_nodes >= 3:
            for i in range(3, l_nodes):
                label = nodes[i]
                if label[-1] == ",":
                    label = label[:-1]
                G.add_edge(nodes[0], label)
    if DBG:
        print(G.nodes, G.edges)

    return G


def boom_part1(input_val, DBG=True):

    G = create_graph(input_val, DBG)
    root_nodes = [node for node in G.nodes() if G.in_degree(node) == 0]

    if DBG:
        print("Root node(s):", root_nodes)
    return root_nodes[0]


def get_downstream_weight(G, child):

    total_weight = G.nodes[child]["weight"]
    children = G.successors(child)

    for child in children:
        total_weight += get_downstream_weight(G, child)

    return total_weight


def recurse(root, G, n2w, DBG=True):
    cur_node = root
    weights = []

    children = G.successors(cur_node)
    lc = list(children)

    for child in lc:
        wei = get_downstream_weight(G, child)
        weights.append(wei)
        if DBG:
            print(child, wei)

    n2w[cur_node] = weights

    unique_elements, counts = np.unique(weights, return_counts=True)
    different_weight = unique_elements[np.argmin(counts)]

    if len(counts) == 1:
        up = list(G.predecessors(cur_node))[0]
        up_weights = n2w[up]
        unique_elements, counts = np.unique(up_weights, return_counts=True)
        different_weight = unique_elements[np.argmin(counts)]
        common_weight = unique_elements[np.argmax(counts)]
        delta = common_weight - different_weight
        return G.nodes[cur_node]["weight"] + delta
    else:
        indices = np.where(weights == different_weight)[0]
        return recurse(lc[indices[0]], G, n2w, DBG)


def boom_part2(input_val, DBG=True):
    G = create_graph(input_val, DBG)
    root = [node for node in G.nodes() if G.in_degree(node) == 0][0]
    n2w = {}
    ret = recurse(root, G, n2w, DBG)
    return ret


# Test cases
#############


t1 = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, "tknk", True)
test_func(boom_part2, tt1, 60, True)

# Real data
############

puzzle_input = read_input_file("input-d07.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = dtacyn
# PART 2 OK = 521
