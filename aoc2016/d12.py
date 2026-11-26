# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Simple interpreter for the "assembunny" language. Registers a-d start
# at 0; we keep a program counter and execute cpy/inc/dec/jnz until the counter
# leaves the program. cpy and jnz operands can be either an integer literal or a
# register name, so a helper resolves a value. jnz jumps relative to itself.
# The answer is the value in register a at halt.
#
# Part 2: Same program, same interpreter, but register c starts at 1 instead of
# 0. `run` accepts an initial register dict, so we just pass c=1. The answer is
# again the value in register a at halt.


def val(x, regs):
    return regs[x] if x in regs else int(x)


def run(ipt, regs=None):
    prog = [line.split() for line in ipt.strip().split("\n")]
    regs = regs if regs is not None else {"a": 0, "b": 0, "c": 0, "d": 0}
    pc = 0
    while 0 <= pc < len(prog):
        ins = prog[pc]
        op = ins[0]
        if op == "cpy":
            regs[ins[2]] = val(ins[1], regs)
        elif op == "inc":
            regs[ins[1]] += 1
        elif op == "dec":
            regs[ins[1]] -= 1
        elif op == "jnz":
            if val(ins[1], regs) != 0:
                pc += val(ins[2], regs)
                continue
        pc += 1
    return regs["a"]


ipt_test = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""

ipt_puzzle = open("input.txt").read().strip()

assert run(ipt_test) == 42

print("Part 1:", run(ipt_puzzle))
print("Part 2:", run(ipt_puzzle, {"a": 0, "b": 0, "c": 1, "d": 0}))

# Part 1 solution: 318083
# Part 2 solution: 9227737
