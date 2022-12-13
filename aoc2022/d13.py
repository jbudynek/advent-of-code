# coding: utf-8

import ast
import functools

from boilerplate import read_input_file, run_func, test_func


def parse_signal(line):
    ret = ast.literal_eval(line)
    return ret


def compare(lhs, rhs):
    if isinstance(lhs, int) and isinstance(rhs, int):
        return lhs - rhs
    elif isinstance(lhs, list) and isinstance(rhs, list):
        lhs_l = len(lhs)
        rhs_l = len(rhs)
        min_l = min(lhs_l, rhs_l)
        for i in range(min_l):
            c = compare(lhs[i], rhs[i])
            if c != 0:
                return c
        return compare(lhs_l, rhs_l)
    else:
        if isinstance(lhs, int):
            return compare([lhs], rhs)
        else:
            return compare(lhs, [rhs])
    return None


def boom_part1(input_val, DBG=True):
    nb_pairs = (len(input_val) + 1) // 3
    ret = 0
    for idx in range(nb_pairs):
        lhs = parse_signal(input_val[idx * 3])
        rhs = parse_signal(input_val[idx * 3 + 1])
        if compare(lhs, rhs) < 0:
            ret += idx + 1

    return ret


def boom_part2(input_val, DBG=True):
    nb_pairs = (len(input_val) + 1) // 3
    all_signals = []
    for idx in range(nb_pairs):
        lhs = parse_signal(input_val[idx * 3])
        rhs = parse_signal(input_val[idx * 3 + 1])
        all_signals.append(lhs)
        all_signals.append(rhs)

    div2 = parse_signal("[[2]]")
    div6 = parse_signal("[[6]]")

    all_signals.append(div2)
    all_signals.append(div6)

    sorted_l = sorted(all_signals, key=functools.cmp_to_key(compare))

    return (1 + sorted_l.index(div2)) * (1 + sorted_l.index(div6))


# Test cases
##########


t1 = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 13, True)
test_func(boom_part2, tt1, 140, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d13.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 5852
# PART 2 OK = 24190
