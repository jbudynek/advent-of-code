# coding: utf-8

import networkx as nx
from boilerplate import read_input_file, run_func, test_func


def parse_slopes(ccc, DBG=True):
    x_max, y_max = len(ccc[0]), len(ccc)

    field = {}
    start, end = 0, 0
    for y, line in enumerate(ccc):
        for x, c in enumerate(line):
            if c != "#":
                field[complex(x, y)] = c
            if y == 0 and x == 1:
                start = complex(x, y)
            if y == y_max - 1 and x == x_max - 2:
                end = complex(x, y)
    if DBG:
        print(field)

    return field, start, end


def make_graph(field):
    # part 1 = if <>v^ you can follow only this direction
    dirs = [complex(0, 1) ** i for i in range(4)]
    v2d = {">": dirs[0], "v": dirs[1], "<": dirs[2], "^": dirs[3]}
    G = nx.DiGraph()
    for z, v in field.items():
        if v == ".":
            for d in dirs:
                nz = z + d
                if nz in field:
                    G.add_edge(z, nz)
        elif v in "^>v<":
            nz = z + v2d[v]
            if nz in field:
                G.add_edge(z, nz)
    return G


def make_graph2(field):
    # part 2 = full graph
    dirs = [complex(0, 1) ** i for i in range(4)]
    G = nx.DiGraph()
    for z, v in field.items():
        if v == "." or v in "^>v<":
            for d in dirs:
                nz = z + d
                if nz in field:
                    G.add_edge(z, nz, weight=1)
    return G


def simplify_graph(G: nx.DiGraph):
    # look for nodes with in and out degree == 2,
    # replace it with longer edges to diminish number of nodes.

    merged = True
    while merged:
        merged = False
        nc = list(G.nodes).copy()
        for nn in nc:
            if G.in_degree(nn) == 2 and G.out_degree(nn) == 2:
                ups, downs = set(G.predecessors(nn)), set(G.successors(nn))
                assert ups == downs
                up = ups.pop()
                down = ups.pop()
                G.add_edge(
                    up,
                    down,
                    weight=(
                        G.get_edge_data(up, nn)["weight"]
                        + G.get_edge_data(nn, down)["weight"]
                    ),
                )
                G.add_edge(
                    down,
                    up,
                    weight=(
                        G.get_edge_data(down, nn)["weight"]
                        + G.get_edge_data(nn, up)["weight"]
                    ),
                )
                G.remove_node(nn)
                merged = True
    return G


def boom_part1(ipt, DBG=True):
    field, start, end = parse_slopes(ipt, DBG)

    G = make_graph(field)

    all_paths = nx.all_simple_paths(G, start, end)
    ans = max(len(p) - 1 for p in all_paths)
    return ans


def boom_part2(ipt, DBG=True):
    field, start, end = parse_slopes(ipt, DBG)

    G = make_graph2(field)

    G = simplify_graph(G)

    all_lengths = []

    paths = nx.all_simple_paths(G, start, end)
    for path in paths:
        total_length = 0
        for i in range(len(path) - 1):
            source, target = path[i], path[i + 1]
            edge = G[source][target]
            length = edge["weight"]
            total_length += length
        all_lengths.append(total_length)

    return max(all_lengths)


# Test cases
#############


ipt_test1 = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()
test_func(boom_part1, ipt_test1, 94, True)
test_func(boom_part2, ipt_test1, 154, True)

# Real data
############

ipt_puzzle = read_input_file("input-d23.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 1966
# Part 2 solution: 6286
# (1 minute)
