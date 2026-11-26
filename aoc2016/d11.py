# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: BFS over states (elevator floor, multiset of (generator floor, chip floor)
# pairs). Elements are interchangeable, so the pairs are kept sorted, which collapses
# symmetric states and keeps the search small. From a state, move one or two items
# from the elevator's floor up or down by one floor; a state is valid if on every
# floor, any chip without its own generator there does not share the floor with a
# generator. The answer is the BFS depth at which all items are on floor 4.
# Part 2: two extra element pairs (elerium, dilithium) start on floor 1; same BFS.

import re
from collections import deque
from itertools import combinations

ipt_test = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""
ipt_puzzle = open("input.txt").read().strip()


def parse(ipt, extra_pairs=0):
    gen, chip = {}, {}
    for f, line in enumerate(ipt.splitlines()):
        for e in re.findall(r"(\w+) generator", line):
            gen[e] = f
        for e in re.findall(r"(\w+)-compatible microchip", line):
            chip[e] = f
    pairs = [(gen[e], chip[e]) for e in gen] + [(0, 0)] * extra_pairs
    return tuple(sorted(pairs))


def valid(pairs):
    gens = {g for g, c in pairs}
    return all(g == c or c not in gens for g, c in pairs)


def solve(ipt, extra_pairs=0):
    start = (0, parse(ipt, extra_pairs))
    n = len(start[1])
    goal = (3, tuple([(3, 3)] * n))
    seen = {start}
    q = deque([(start, 0)])
    while q:
        (e, pairs), d = q.popleft()
        if (e, pairs) == goal:
            return d
        # items as (pair index, 0=generator / 1=chip) located on the elevator floor
        items = [(i, k) for i, p in enumerate(pairs) for k in (0, 1) if p[k] == e]
        moves = [(x,) for x in items] + list(combinations(items, 2))
        for ne in (e - 1, e + 1):
            if not 0 <= ne <= 3:
                continue
            for mv in moves:
                new = [list(p) for p in pairs]
                for i, k in mv:
                    new[i][k] = ne
                np_ = tuple(sorted(tuple(p) for p in new))
                s = (ne, np_)
                if s not in seen and valid(np_):
                    seen.add(s)
                    q.append((s, d + 1))


assert solve(ipt_test) == 11
print(solve(ipt_puzzle))
print(solve(ipt_puzzle, 2))

# Part 1 solution: 47
# Part 2 solution: 71
