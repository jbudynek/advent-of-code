# coding: utf-8
import networkx as nx
from boilerplate import read_input_file, run_func, test_func


def create_world(input, DBG=True):

    x_max, y_max = len(input[0]), len(input)

    field = {
        complex(y, x): (ord(input[y][x]) - ord("a"))
        for y in range(y_max)
        for x in range(x_max)
    }

    for z in field.keys():
        if field[z] == ord("S") - ord("a"):
            start = z
            field[z] = ord("a") - ord("a")
        elif field[z] == ord("E") - ord("a"):
            end = z
            field[z] = ord("z") - ord("a")

    if DBG:
        print(field)

    return field, start, end


def create_network(input_val, DBG):
    field, start, end = create_world(input_val, DBG)
    digraph = nx.DiGraph()
    for z in field.keys():
        adj = [(z + complex(0, 1) ** idx) for idx in range(4)]
        for d in adj:
            if d in field and ((field[d] - field[z] == 1) or (field[d] <= field[z])):
                digraph.add_edge(z, d)
    if DBG:
        print(digraph.nodes)
        print(digraph.edges)
    return digraph, field, start, end


def get_shortest_path_length(graph, starters, end):
    lens = []
    for s in starters:
        try:
            spl = nx.shortest_path_length(graph, source=s, target=end)
            lens.append(spl)
        except nx.exception.NetworkXNoPath:
            pass
    return min(lens)


def boom_part1(input_val, DBG=True):
    graph, _, start, end = create_network(input_val, DBG)
    starters = [start]
    return get_shortest_path_length(graph, starters, end)


def boom_part2(input_val, DBG=True):
    graph, field, _, end = create_network(input_val, DBG)
    starters = [n for n in graph.nodes if field[n] == 0]
    return get_shortest_path_length(graph, starters, end)


# Test cases
##########


t1 = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 31, True)
test_func(boom_part2, tt1, 29, True)

# Real data
##########

puzzle_input = read_input_file("input-d12.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 504
# PART 2 OK = 500
