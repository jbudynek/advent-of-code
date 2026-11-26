# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: BFS from every numbered location to get pairwise shortest distances,
# then try every visiting order of the non-0 locations (permutations, TSP by brute
# force) starting at 0, and keep the shortest total.
# Part 2: same, but the route must also return to 0 at the end.

from collections import deque
from itertools import permutations

ipt_test = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""
ipt_puzzle = open("input.txt").read().strip()


def distances(ipt):
    grid = ipt.splitlines()
    pois = {c: (x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c.isdigit()}
    dist = {}
    for a, start in pois.items():
        seen = {start: 0}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in seen and grid[n[1]][n[0]] != "#":
                    seen[n] = seen[(x, y)] + 1
                    q.append(n)
        for b, p in pois.items():
            dist[a, b] = seen[p]
    return dist, sorted(pois)


def shortest(ipt, back):
    dist, names = distances(ipt)
    others = [n for n in names if n != "0"]
    best = None
    for perm in permutations(others):
        route = ("0",) + perm + (("0",) if back else ())
        d = sum(dist[a, b] for a, b in zip(route, route[1:]))
        if best is None or d < best:
            best = d
    return best


assert shortest(ipt_test, False) == 14
print(shortest(ipt_puzzle, False))
assert shortest(ipt_test, True) == 20
print(shortest(ipt_puzzle, True))

# Part 1 solution: 428
# Part 2 solution: 680
