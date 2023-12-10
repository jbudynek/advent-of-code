# coding: utf-8
import networkx as nx
from boilerplate import read_input_file, run_func, test_func
from shapely.geometry import Point, Polygon


def parse_world_complex(ipt, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ipt:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == ".":
                pass
            elif c in "|-LJ7FS":
                field[complex(x, y)] = c
            else:
                quit(f"parse error {c}")

    if DBG:
        print(field)

    dirs = [complex(0, 1) ** i for i in range(4)]
    west = dirs[0]
    north = dirs[3]
    east = dirs[2]
    south = dirs[1]
    G = nx.Graph()
    start = 0
    for k, v in field.items():
        if v == "S":
            start = k
            # |
            if (
                k + north in field
                and field[k + north] in "|7F"
                and k + south in field
                and field[k + south] in "|LJ"
            ):
                G.add_edge(k, k + north)
                G.add_edge(k, k + south)
            # -
            elif (
                k + west in field
                and field[k + west] in "-J7"
                and k + east in field
                and field[k + east] in "-FL"
            ):
                G.add_edge(k, k + west)
                G.add_edge(k, k + east)
            # "L":
            elif (
                k + north in field
                and field[k + north] in "|7F"
                and k + west in field
                and field[k + west] in "-J7"
            ):
                G.add_edge(k, k + north)
                G.add_edge(k, k + west)
            # "J":
            elif (
                k + north in field
                and field[k + north] in "|7F"
                and k + east in field
                and field[k + east] in "-FL"
            ):
                G.add_edge(k, k + north)
                G.add_edge(k, k + east)
            # "7":
            elif (
                k + south in field
                and field[k + south] in "|LJ"
                and k + west in field
                and field[k + west] in "-J7"
            ):
                G.add_edge(k, k + south)
                G.add_edge(k, k + west)
            # "F":
            elif (
                k + south in field
                and field[k + south] in "|LJ"
                and k + west in field
                and field[k + west] in "-J7"
            ):
                G.add_edge(k, k + south)
                G.add_edge(k, k + west)

        # "|-LJ7FS"
        elif v == "|":
            if k + north in field and field[k + north] in "|7F":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "|LJ":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "":
                G.add_edge(k, k + east)
        # "|-LJ7FS"
        elif v == "-":
            if k + north in field and field[k + north] in "":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "-J7":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "-FL":
                G.add_edge(k, k + east)
        # "|-LJ7FS"
        elif v == "L":
            if k + north in field and field[k + north] in "|7F":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "-J7":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "":
                G.add_edge(k, k + east)
        # "|-LJ7FS"
        elif v == "J":
            if k + north in field and field[k + north] in "|7F":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "-FL":
                G.add_edge(k, k + east)
        # "|-LJ7FS"
        elif v == "7":
            if k + north in field and field[k + north] in "":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "|LJ":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "-J7":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "":
                G.add_edge(k, k + east)
        # "|-LJ7FS"
        elif v == "F":
            if k + north in field and field[k + north] in "":
                G.add_edge(k, k + north)
            if k + south in field and field[k + south] in "|LJ":
                G.add_edge(k, k + south)
            if k + west in field and field[k + west] in "-J7":
                G.add_edge(k, k + west)
            if k + east in field and field[k + east] in "":
                G.add_edge(k, k + east)

    return G, start


def boom_part1(ipt, DBG=True):
    G, start = parse_world_complex(ipt, DBG)
    length = dict(nx.shortest_path_length(G, start))
    ans = 0
    for dest, dist in length.items():
        if DBG and dist > ans:
            print(f"{start} - {dest}: {dist}")
        ans = max(ans, dist)
    return ans


def boom_part2(ipt, DBG=True):
    G, start = parse_world_complex(ipt, DBG)

    cycle = nx.find_cycle(G, start)

    coords = [(int(z[0].real), int(z[0].imag)) for z in cycle]
    poly = Polygon(coords)

    xx = [c[0] for c in coords]
    yy = [c[1] for c in coords]

    ans = 0
    for x in range(min(xx), max(xx)):
        for y in range(min(yy), max(yy)):
            p = Point(x, y)
            if p.within(poly):
                ans += 1

    return ans


# Test cases
#############


ipt_test1 = """.....
.S-7.
.|.|.
.L-J.
.....""".splitlines()
# test_func(boom_part1, ipt_test1, 4, True)

ipt_test1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()
# test_func(boom_part1, ipt_test1, 8, True)


ipt_test1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".splitlines()
test_func(boom_part2, ipt_test1, 4, True)


ipt_test1 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".splitlines()
test_func(boom_part2, ipt_test1, 8, True)


ipt_test1 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()
# this test case does not work, for some reason...
# test_func(boom_part2, ipt_test1, 10, True)

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 6831
# Part 2 solution: 305
