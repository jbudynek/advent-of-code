# coding: utf-8
import math
import re

from boilerplate import read_input_file, run_func, test_func


def parse_world(ipt):
    dirs = ipt[0]
    node2nodes = {}
    for line in ipt[2:]:
        ss = re.split(r"[ ,()=]+", line)
        node2nodes[ss[0]] = (ss[1], ss[2])
    return dirs, node2nodes


def get_cycle_length(start_node, dirs, node2nodes, end_nodes):
    step = 0
    cur_node = start_node
    while True:
        if cur_node in end_nodes:
            return step
        lr = node2nodes[cur_node]
        if dirs[step % len(dirs)] == "L":
            cur_node = lr[0]
        else:
            cur_node = lr[1]
        step += 1


def boom_part1(ipt, DBG=True):
    dirs, node2nodes = parse_world(ipt)
    return get_cycle_length("AAA", dirs, node2nodes, ["ZZZ"])


def boom_part2(ipt, DBG=True):
    dirs, node2nodes = parse_world(ipt)
    start_nodes = []
    end_nodes = []
    for node in node2nodes.keys():
        if node.endswith("A"):
            start_nodes.append(node)
        if node.endswith("Z"):
            end_nodes.append(node)
    ans = 1
    for start_node in start_nodes:
        cycle_length = get_cycle_length(start_node, dirs, node2nodes, end_nodes)
        ans = math.lcm(ans, cycle_length)
    return ans


# Test cases
#############


ipt_test1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".splitlines()
test_func(boom_part1, ipt_test1, 2, True)

ipt_test1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".splitlines()
test_func(boom_part1, ipt_test1, 6, True)


ipt_test1 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".splitlines()

test_func(boom_part2, ipt_test1, 6, True)

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

# Part 1 solution: 19099
# Part 2 solution: 17099847107071
