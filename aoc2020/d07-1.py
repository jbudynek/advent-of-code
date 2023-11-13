# coding: utf-8
import time

import networkx as nx


def create_world(rules, DBG=True):
    world = nx.DiGraph()

    # light red bags contain 1 bright white bag, 2 muted yellow bags.

    for rule in rules:
        words = rule.split(" ")
        node0_name = words[0] + " " + words[1]
        world.add_node(node0_name)
        if DBG:
            print(node0_name)
        i = 4
        while i < len(words):
            node_name = words[i + 1] + " " + words[i + 2]
            if words[i] == "no":
                break
            node_weight = int(words[i])
            world.add_edge(node0_name, node_name, weight=node_weight)
            i = i + 4
            if DBG:
                print(node_name, node_weight)

    if DBG:
        print(
            world.number_of_nodes(),
            world.number_of_edges(),
            list(world.nodes),
            list(world.edges),
        )
    return world


def get_all_parents(node, world, DBG=True):
    up = list(world.predecessors(node))
    if DBG:
        print(node, up)
    if len(up) == 0:
        return {}
    else:
        ret = {}
        for up_node in up:
            ret.update(get_all_parents(up_node, world, DBG).items())
            ret[up_node] = 1
        if DBG:
            print(ret)
        return ret


def boom(input_val, DBG=True):
    rules = input_val
    world = create_world(rules, DBG)
    nb_colors = 0

    node = "shiny gold"  # RECURSE
    if DBG:
        print(node)
    nb_colors = len(get_all_parents(node, world, DBG))

    return nb_colors


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


t1 = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
tt1 = t1.splitlines()
test(tt1, 4, True)
# sys.exit()

INPUT_FILE = "input-d07.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 2 = 300
