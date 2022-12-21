# coding: utf-8
import sys

from boilerplate import read_input_file, run_func, test_func
from sympy.solvers import solve


def unfold(key, ops):
    t = ops[key]
    tt = t.split()
    if len(tt) == 1:
        return "int(" + tt[0] + ")"
    else:
        return "(" + unfold(tt[0], ops) + tt[1] + unfold(tt[2], ops) + ")"


def unfold2(key, ops):
    if key == "humn":
        return "(x)"
    t = ops[key]
    tt = t.split()
    if len(tt) == 1:
        return "(" + tt[0] + ")"
    else:
        return "(" + unfold2(tt[0], ops) + tt[1] + unfold2(tt[2], ops) + ")"


def boom_part1(input_val, DBG=True):
    ops = {}
    for line in input_val:
        ll = line.split(":")
        ops[ll[0]] = ll[1]
    expr = unfold("root", ops)
    ret = int(eval(expr))

    return ret


def boom_part2(input_val, DBG=True):
    ops = {}
    for line in input_val:
        ll = line.split(":")
        ops[ll[0]] = ll[1]

    t = ops["root"]
    tt = t.split()

    k1 = tt[0]
    k2 = tt[2]

    expr1 = unfold2(k1, ops)
    expr2 = unfold2(k2, ops)
    if DBG:
        print(expr1)
    if DBG:
        print(expr2)

    r = solve(expr1 + "-" + expr2)

    return r[0]


# Test cases
##########


t1 = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 152, True)
test_func(boom_part2, tt1, 301, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d21.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 145167969204648
# PART 2 OK = 3330805295850

sys.exit()
