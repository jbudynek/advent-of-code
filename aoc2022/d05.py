# coding: utf-8
import re
from collections import defaultdict, deque

from boilerplate import read_input_file, run_func, test_func


def make_world(input_val, DBG=True):
    stacks = defaultdict(deque)
    idx = 0
    while True:
        line = input_val[idx]
        idx += 1
        if line.startswith(" 1 "):
            idx += 1
            break
        for j in range((1 + len(line)) // 4):
            if line[j * 4 + 1] != " ":
                stacks[j + 1].appendleft(line[j * 4 + 1])
    if DBG:
        print(stacks)

    instructions = []
    while idx < len(input_val):
        line = input_val[idx]
        idx += 1
        nb_crates, from_stack, to_stack = map(int, re.findall(r"\d+", line))
        instructions.append((nb_crates, from_stack, to_stack))
    if DBG:
        print(instructions)

    return (stacks, instructions)


def process_instructions(stacks, instructions, reverse=False):
    for inst in instructions:
        (nb_crates, from_stack, to_stack) = inst
        crates_list = []
        for _ in range(nb_crates):
            crate = stacks[from_stack].pop()
            crates_list.append(crate)
        if reverse:
            crates_list = reversed(crates_list)
        stacks[to_stack].extend(crates_list)

    return stacks


def get_top_crates(stacks):
    ret = ""
    for i in range(len(stacks.keys())):
        ret += stacks[i + 1][-1]
    return ret


def boom_part1(input_val, DBG=True):
    (stacks, instructions) = make_world(input_val, DBG)

    stacks = process_instructions(stacks, instructions, False)

    return get_top_crates(stacks)


def boom_part2(input_val, DBG=True):
    (stacks, instructions) = make_world(input_val, DBG)

    stacks = process_instructions(stacks, instructions, True)

    return get_top_crates(stacks)


# Test cases
##########


t1 = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""  # noqa
tt1 = t1.splitlines()
test_func(boom_part1, tt1, "CMZ", True)
test_func(boom_part2, tt1, "MCD", True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d05.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = GFTNRBZPF
# PART 2 OK = VRQWPDSGP
