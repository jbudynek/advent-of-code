# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: parse every node into (x, y, size, used, avail), then count ordered pairs
# (A, B) with A != B, used(A) > 0 and used(A) <= avail(B).
# Part 2: the grid is a sliding puzzle. There is a single empty node; nodes whose
# data is larger than the empty node's size are immovable walls, all others are
# interchangeable. BFS over the state (empty position, goal data position) where a
# move swaps the empty node with an adjacent non-wall node (carrying the goal data
# if it is swapped), until the goal data reaches (0, 0).

import re
from collections import deque

ipt_test = """Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""
ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    nodes = []
    for line in ipt.splitlines():
        m = re.match(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line)
        if m:
            nodes.append(tuple(int(g) for g in m.groups()))
    return nodes


def viable_pairs(ipt):
    nodes = parse(ipt)
    n = 0
    for i, a in enumerate(nodes):
        if a[3] == 0:
            continue
        for j, b in enumerate(nodes):
            if i != j and a[3] <= b[4]:
                n += 1
    return n


assert viable_pairs(ipt_test) == 7
print(viable_pairs(ipt_puzzle))


def fewest_steps(ipt):
    nodes = parse(ipt)
    grid = {(x, y): (size, used) for x, y, size, used, _ in nodes}
    empty = next(p for p, (s, u) in grid.items() if u == 0)
    cap = grid[empty][0]
    walls = {p for p, (s, u) in grid.items() if u > cap}
    gx = max(x for x, y in grid)
    start = (empty, (gx, 0))
    seen = {start}
    q = deque([(start, 0)])
    while q:
        (e, g), d = q.popleft()
        if g == (0, 0):
            return d
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (e[0] + dx, e[1] + dy)
            if n not in grid or n in walls:
                continue
            ns = (n, e if n == g else g)
            if ns not in seen:
                seen.add(ns)
                q.append((ns, d + 1))


assert fewest_steps(ipt_test) == 7
print(fewest_steps(ipt_puzzle))

# Part 1 solution: 981
# Part 2 solution: 233
