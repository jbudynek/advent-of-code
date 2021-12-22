# coding: utf-8
from collections import defaultdict
from timeit import default_timer as timer

# Main function
##########


def parse_input(ll):
    rules = {}
    for l in ll:
        ls = l.split(" -> ")
        rules[ls[0]] = ls[1]
    return rules


def run_steps(input_val, nb_steps, DBG=True):
    template = input_val[0]

    rules = parse_input(input_val[2:])

    # we count pairs!
    pair_count = defaultdict(int)
    for i in range(len(template)-1):
        pair = template[i]+template[i+1]
        pair_count[pair] += 1

    step = 0
    while step < nb_steps:
        step += 1
        new_pair_count = pair_count.copy()
        for pair in pair_count.keys():
            new_pair_lhs = pair[0]+rules[pair]
            new_pair_rhs = rules[pair]+pair[1]
            new_pair_count[new_pair_lhs] += pair_count[pair]
            new_pair_count[new_pair_rhs] += pair_count[pair]
            new_pair_count[pair] -= pair_count[pair]
        pair_count = new_pair_count

    # now count characters, only count right side of pair
    char_count = defaultdict(int)
    for pair in pair_count.keys():
        rhs = pair[1]
        ct = pair_count[pair]
        char_count[rhs] += ct

    # and add first left character
    char_count[template[0]] += 1

    return max(char_count.values())-min(char_count.values())


def boom_part1(input_val, DBG=True):
    return run_steps(input_val, 10, DBG)


def boom_part2(input_val, DBG=True):
    return run_steps(input_val, 40, DBG)

# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
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


tt1 = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
tt1 = tt1.splitlines()
test_part1(tt1, 1588, True)
test_part2(tt1, 2188189693529, True)

# Real data
##########

INPUT_FILE = "input-d14.txt"
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

# PART 1 OK = 2915
# PART 2 OK = 3353146900153
