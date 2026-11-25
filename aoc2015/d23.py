# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# A tiny interpreter for a two-register machine (a and b, both starting at 0).
# The program is parsed into a list of (op, args); a program counter `pc` walks
# through it. hlf/tpl/inc modify a register and go to the next instruction; jmp,
# jie (jump if even) and jio (jump if exactly one) add an offset to `pc`.
# The program stops when `pc` leaves the instruction list.
# - Part 1: run from a = 0, b = 0 and return the final value of b.
# - Part 2: same interpreter, but register a starts at 1.

ipt_test = """inc a
jio a, +2
tpl a
inc a"""

ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    prog = []
    for line in ipt.splitlines():
        op, rest = line.split(" ", 1)
        prog.append((op, [x.strip() for x in rest.split(",")]))
    return prog


def run(prog, a=0, b=0):
    reg = {"a": a, "b": b}
    pc = 0
    while 0 <= pc < len(prog):
        op, args = prog[pc]
        if op == "hlf":
            reg[args[0]] //= 2
        elif op == "tpl":
            reg[args[0]] *= 3
        elif op == "inc":
            reg[args[0]] += 1
        elif op == "jmp":
            pc += int(args[0])
            continue
        elif op == "jie":
            if reg[args[0]] % 2 == 0:
                pc += int(args[1])
                continue
        elif op == "jio":
            if reg[args[0]] == 1:
                pc += int(args[1])
                continue
        pc += 1
    return reg


# test
r_test1 = run(parse(ipt_test))["a"]
print(f"# Test part 1: {r_test1} (expected 2)")
assert r_test1 == 2

# test part 2: the example has no part 2 value; starting with a = 1 the example
# program does inc a (2), jio a,+2 not taken (a != 1), tpl a (6), inc a (7)
r_test2 = run(parse(ipt_test), a=1)["a"]
print(f"# Test part 2: {r_test2} (expected 7)")
assert r_test2 == 7

r1 = run(parse(ipt_puzzle))["b"]
print(f"# Part 1 solution: {r1}")
r2 = run(parse(ipt_puzzle), a=1)["b"]
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 170
# Part 2 solution: 247
