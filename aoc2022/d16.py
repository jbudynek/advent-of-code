# coding: utf-8
import copy
import sys
from functools import cache
from itertools import combinations

import networkx as nx
from boilerplate import print_time, read_input_file, run_func, test_func, timer

# build network
# build all-to-all shortest paths, that's the distance
# PART 1:
# do a depth-first-search, with memoization (use @cache annotation!)
# return early in the dfs
# PART 2:
# separate the nodes in partitions of two sets, one for me, one for the elephant
# (do this using combinations)
# then do a depth-first-search on each set and sum the results

DISTANCE = {}
RATES = {}


def build_net(ipt, DBG=True):
    global DISTANCE
    global RATES
    net = nx.Graph()
    for line in ipt:
        words = line.split()
        v0 = words[1]
        rate = int(words[4].split("=")[1][:-1])
        vv = words[9:]
        net.add_node(v0, rate=rate)
        for v in vv:
            net.add_edge(v0, v[0:2])
    if DBG:
        print(net.nodes, net.edges)
    DISTANCE = dict(nx.all_pairs_shortest_path_length(net))
    RATES = dict(net.nodes(data="rate"))
    return net


@cache
def depth_first_search(current_node, remaining_nodes_to_open, remaining_time):
    global DISTANCE
    global RATES

    all_pressures = [0]
    for next_node in remaining_nodes_to_open:
        # remove one node from list and recurse
        rem_list = list(copy.deepcopy(remaining_nodes_to_open))
        rem_list.remove(next_node)
        next_remaining_list = tuple(rem_list)
        # if you're close enough to reach this node, recurse
        # time decreases by the distance, and 1 more step to open the valve.
        if (DISTANCE[current_node][next_node] + 1) <= remaining_time:
            pressure = RATES[next_node] * (
                remaining_time - (DISTANCE[current_node][next_node] + 1)
            ) + depth_first_search(
                next_node,
                next_remaining_list,
                remaining_time - (DISTANCE[current_node][next_node] + 1),
            )
            all_pressures.append(pressure)
    return max(all_pressures)


def boom_part1(input_val, DBG=True):
    global DISTANCE
    global RATES

    net = build_net(input_val, DBG)

    all_nodes = list(copy.deepcopy(net.nodes))
    # remove nodes with flow=0
    for node in net.nodes:
        if RATES[node] == 0:
            all_nodes.remove(node)

    max_pressure = depth_first_search("AA", tuple(all_nodes), 30)

    return max_pressure


def boom_part2(input_val, DBG=True):
    global DISTANCE
    global RATES

    net = build_net(input_val, DBG)

    all_nodes = list(copy.deepcopy(net.nodes))
    # remove nodes with flow=0
    for node in net.nodes:
        if RATES[node] == 0:
            all_nodes.remove(node)

    ll = len(all_nodes)

    max_total_pressure = 0

    # only go to half, as the elephant and I are interchangeable
    for nb_nodes_for_me in range(1, ll // 2 + 1):
        t_start = timer()
        if DBG:
            print("*", nb_nodes_for_me, "/", ll // 2 + 1)
        for c in combinations(all_nodes, nb_nodes_for_me):
            nodes_me = tuple(c)
            nodes_elephant = tuple(set(all_nodes) - set(c))
            pressure_me = depth_first_search("AA", tuple(nodes_me), 26)
            pressure_elephant = depth_first_search("AA", tuple(nodes_elephant), 26)
            max_total_pressure = max(
                max_total_pressure, pressure_me + pressure_elephant
            )
        if DBG:
            print(">", max_total_pressure)
        t_end = timer()
        if DBG:
            print_time(t_start, t_end)
    return max_total_pressure


# Test cases
##########


t1 = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 1651, True)
# sys.exit()
test_func(boom_part2, tt1, 1707, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d16.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=True)

print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

sys.exit()

# PART 1 OK = 1767
# PART 2 OK = 2528
