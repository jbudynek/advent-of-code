# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Disc i (1-indexed) with n positions starting at position p is open
# for a button press at time t when (p + t + i) % n == 0. Simulate: step t
# upward from 0 and return the first t for which every disc is open.
#
# Part 2: Append a disc with 11 positions at position 0 below the last one,
# then solve the same way. To stay fast, sieve: once a disc is satisfied at t,
# only step by the product of the moduli handled so far (Chinese remainder idea).
import re

ipt_test = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""
ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    return [
        tuple(map(int, re.findall(r"\d+", line))) for line in ipt.splitlines()
    ]


def solve(ipt, extra=False):
    discs = parse(ipt)
    if extra:
        discs.append((len(discs) + 1, 11, 0, 0))
    t, step = 0, 1
    for i, n, _, p in discs:
        while (p + t + i) % n != 0:
            t += step
        step *= n
    return t


assert solve(ipt_test) == 5
print("Part 1:", solve(ipt_puzzle))
# the example with the extra disc: discs (5,4), (2,1), (11,0)
assert solve(ipt_test, True) == 85
print("Part 2:", solve(ipt_puzzle, True))

# Part 1 solution: 121834
# Part 2 solution: 3208099
