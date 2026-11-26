# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Breadth-first search on the infinite maze starting at (1,1). A cell
# (x,y) is open when the popcount of x*x + 3x + 2xy + y + y*y + favorite is
# even; negative coordinates are invalid. BFS explores neighbours level by
# level, so the first time we reach the target, the step count is minimal.
#
# Part 2: Same BFS, but instead of stopping at a target we run exactly 50
# levels and count all distinct cells seen (including the start).


def is_open(x, y, fav):
    if x < 0 or y < 0:
        return False
    return bin(x * x + 3 * x + 2 * x * y + y + y * y + fav).count("1") % 2 == 0


def bfs(fav, target):
    seen = {(1, 1)}
    frontier = [(1, 1)]
    steps = 0
    while frontier:
        if target in frontier:
            return steps
        nxt = []
        for x, y in frontier:
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) not in seen and is_open(nx, ny, fav):
                    seen.add((nx, ny))
                    nxt.append((nx, ny))
        frontier = nxt
        steps += 1


def reachable(fav, max_steps):
    seen = {(1, 1)}
    frontier = [(1, 1)]
    for _ in range(max_steps):
        nxt = []
        for x, y in frontier:
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) not in seen and is_open(nx, ny, fav):
                    seen.add((nx, ny))
                    nxt.append((nx, ny))
        frontier = nxt
    return len(seen)


ipt_test = "10"
ipt_puzzle = open("input.txt").read().strip()

assert bfs(int(ipt_test), (7, 4)) == 11

print("Part 1:", bfs(int(ipt_puzzle), (31, 39)))
print("Part 2:", reachable(int(ipt_puzzle), 50))

# Part 1 solution: 92
# Part 2 solution: 124
