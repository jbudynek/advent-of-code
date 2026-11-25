# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: implement the 16 opcodes as functions (regs, a, b) -> value to store.
# Parse the input's first section into samples (before, instruction, after).
# For each sample, count how many opcodes, applied to a copy of "before",
# produce exactly "after". Count the samples where at least 3 opcodes match.
#
# Part 2: for each opcode number, intersect the sets of opcode names that fit
# every sample using that number. Then solve like a sudoku: repeatedly take a
# number with a single remaining candidate, fix it, and remove that name from
# the others. Finally run the test program (second section of the input) with
# the resolved mapping and read register 0.

import re

ipt_test = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""
ipt_puzzle = open("input.txt").read().strip()

OPS = {
    "addr": lambda r, a, b: r[a] + r[b],
    "addi": lambda r, a, b: r[a] + b,
    "mulr": lambda r, a, b: r[a] * r[b],
    "muli": lambda r, a, b: r[a] * b,
    "banr": lambda r, a, b: r[a] & r[b],
    "bani": lambda r, a, b: r[a] & b,
    "borr": lambda r, a, b: r[a] | r[b],
    "bori": lambda r, a, b: r[a] | b,
    "setr": lambda r, a, b: r[a],
    "seti": lambda r, a, b: a,
    "gtir": lambda r, a, b: int(a > r[b]),
    "gtri": lambda r, a, b: int(r[a] > b),
    "gtrr": lambda r, a, b: int(r[a] > r[b]),
    "eqir": lambda r, a, b: int(a == r[b]),
    "eqri": lambda r, a, b: int(r[a] == b),
    "eqrr": lambda r, a, b: int(r[a] == r[b]),
}


def parse_samples(s):
    samples = []
    for m in re.finditer(r"Before: \[(.*?)\]\n(.*?)\nAfter:  \[(.*?)\]", s):
        before = [int(x) for x in m.group(1).split(",")]
        ins = [int(x) for x in m.group(2).split()]
        after = [int(x) for x in m.group(3).split(",")]
        samples.append((before, ins, after))
    return samples


def matching(sample):
    before, (_, a, b, c), after = sample
    res = set()
    for name, f in OPS.items():
        regs = before[:]
        regs[c] = f(regs, a, b)
        if regs == after:
            res.add(name)
    return res


def part1(s):
    return sum(len(matching(x)) >= 3 for x in parse_samples(s))


def resolve(samples):
    # candidates[n] = opcode names compatible with every sample of number n;
    # then repeatedly fix the number that has a single candidate left.
    cands = {}
    for sample in samples:
        n = sample[1][0]
        cands[n] = cands.get(n, set(OPS)) & matching(sample)
    mapping = {}
    while cands:
        n = next(k for k, v in cands.items() if len(v) == 1)
        name = cands.pop(n).pop()
        mapping[n] = name
        for v in cands.values():
            v.discard(name)
    return mapping


def part2(s):
    samples_txt, program_txt = s.split("\n\n\n\n")
    mapping = resolve(parse_samples(samples_txt))
    assert len(mapping) == 16 and len(set(mapping.values())) == 16
    regs = [0, 0, 0, 0]
    for line in program_txt.splitlines():
        op, a, b, c = [int(x) for x in line.split()]
        regs[c] = OPS[mapping[op]](regs, a, b)
    return regs[0]


assert matching(parse_samples(ipt_test)[0]) == {"mulr", "addi", "seti"}
assert part1(ipt_test) == 1

# part 2 has no example: sanity check that the opcode mapping resolves fully
# (asserted inside part2).

print("Part 1:", part1(ipt_puzzle))
print("Part 2:", part2(ipt_puzzle))

# Part 1 solution: 500
# Part 2 solution: 533
