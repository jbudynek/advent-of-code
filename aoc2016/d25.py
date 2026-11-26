# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: an assembunny interpreter with the extra "out" instruction. For each
# candidate a = 1, 2, 3, ... run the program until it has emitted 30 values; the
# candidate is good if they are exactly 0, 1, 0, 1, ... (stop at the first wrong
# value). The first good candidate is the answer.
# Part 2: no puzzle to solve; it is unlocked by owning the other 49 stars.

ipt_puzzle = open("input.txt").read().strip()


def good(prog, a, n=30):
    reg = {"a": a, "b": 0, "c": 0, "d": 0}

    def val(x):
        return reg[x] if x in reg else int(x)

    pc, count = 0, 0
    while 0 <= pc < len(prog):
        ins = prog[pc]
        op = ins[0]
        if op == "cpy":
            reg[ins[2]] = val(ins[1])
        elif op == "inc":
            reg[ins[1]] += 1
        elif op == "dec":
            reg[ins[1]] -= 1
        elif op == "jnz":
            if val(ins[1]) != 0:
                pc += val(ins[2])
                continue
        elif op == "out":
            if val(ins[1]) != count % 2:
                return False
            count += 1
            if count == n:
                return True
        pc += 1
    return False


def solve(ipt):
    prog = [l.split() for l in ipt.splitlines()]
    a = 1
    while not good(prog, a):
        a += 1
    return a


# test: a trivial program that outputs 0,1,0,1... forever is accepted for any a
assert good([l.split() for l in "out 0\nout 1\njnz 1 -2".splitlines()], 1)
assert not good([l.split() for l in "out 1\njnz 1 -1".splitlines()], 1)
print(solve(ipt_puzzle))

# Part 1 solution: 175
# Part 2 solution: none (no answer to submit; needs all 49 other stars)
