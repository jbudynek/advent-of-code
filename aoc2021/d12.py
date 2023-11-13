# coding: utf-8
from collections import Counter, deque
from timeit import default_timer as timer

import networkx as nx

# Helpers
##########


def create_network(lll, DBG=True):
    G = nx.Graph()
    small_caves = set()
    big_caves = set()
    for ll in lll:
        nodes = ll.split("-")
        G.add_edge(nodes[0], nodes[1])
        for n in nodes:
            if n.islower():
                small_caves.add(n)
            else:
                big_caves.add(n)
    if DBG:
        print(G.nodes, G.edges)
        print(small_caves)
        print(big_caves)
    return (G, small_caves, big_caves)


# Main function
##########


def count_paths(input_val, max_visit, DBG=True):
    (G, small_caves, big_caves) = create_network(input_val, DBG)

    paths_ok = []

    nodes_queue = deque()
    paths_queue = deque()
    visited_queue = deque()

    for n in G.neighbors("start"):
        path = ["start", n]
        visited = {"start": max_visit}
        if n in small_caves:
            visited[n] = visited.get(n, 0) + 1
        nodes_queue.append(n)
        paths_queue.append(path.copy())
        visited_queue.append(visited.copy())
        while nodes_queue:
            nn = nodes_queue.pop()
            path = paths_queue.pop()
            visited = visited_queue.pop()
            small_caves_with_two_visits = Counter(visited.values())[2]
            for next in G.neighbors(nn):
                npath = path.copy()
                nvisited = visited.copy()
                if (
                    visited.get(next, 0) < max_visit
                    and small_caves_with_two_visits <= 2
                ):
                    if next in small_caves:
                        nvisited[next] = visited.get(next, 0) + 1
                    npath.append(next)
                    if next == "end":
                        paths_ok.append(npath)
                    else:
                        nodes_queue.append(next)
                        paths_queue.append(npath)
                        visited_queue.append(nvisited)

    if DBG:
        print(paths_ok)

    return len(paths_ok)


def boom_part1(input_val, DBG=True):
    return count_paths(input_val, 1, DBG)


def boom_part2(input_val, DBG=True):
    return count_paths(input_val, 2, DBG)


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


tt1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 10, True)
test_part2(tt1, 36, True)

tt2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
tt2 = tt2.splitlines()  # type: ignore
test_part1(tt2, 19, False)
test_part2(tt2, 103, False)

tt3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
tt3 = tt3.splitlines()  # type: ignore
test_part1(tt3, 226, False)
test_part2(tt3, 3509, False)

# Real data
##########

INPUT_FILE = "input-d12.txt"
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

# PART 1 OK = 4707
# PART 2 OK = 130493
