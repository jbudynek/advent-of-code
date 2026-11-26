# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Breadth-first search over (x, y, path) states. At each room, the MD5
# of passcode + path gives the doors: first four hex chars = U, D, L, R; a char
# in "bcdef" means open. Stay inside the 4x4 grid. The first path reaching the
# bottom-right room (3, 3) is the shortest; the vault room is never left.
#
# Part 2: Same exploration, but do not stop at the first arrival: when a state
# reaches the vault, record its path length and do not expand it further
# (the vault room is final). Explore everything and keep the maximum length.
from collections import deque
from hashlib import md5

ipt_test = "ihgpwlah"
ipt_puzzle = open("input.txt").read().strip()

MOVES = (("U", 0, -1), ("D", 0, 1), ("L", -1, 0), ("R", 1, 0))


def neighbors(passcode, x, y, path):
    h = md5((passcode + path).encode()).hexdigest()[:4]
    for c, (d, dx, dy) in zip(h, MOVES):
        nx, ny = x + dx, y + dy
        if c in "bcdef" and 0 <= nx < 4 and 0 <= ny < 4:
            yield nx, ny, path + d


def shortest(passcode):
    q = deque([(0, 0, "")])
    while q:
        x, y, path = q.popleft()
        if (x, y) == (3, 3):
            return path
        q.extend(neighbors(passcode, x, y, path))


assert shortest("ihgpwlah") == "DDRRRD"
assert shortest("kglvqrro") == "DDUDRLRRUDRD"
assert shortest("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"
print("Part 1:", shortest(ipt_puzzle))


def longest(passcode):
    q = deque([(0, 0, "")])
    best = None
    while q:
        x, y, path = q.popleft()
        if (x, y) == (3, 3):
            best = len(path)
            continue
        q.extend(neighbors(passcode, x, y, path))
    return best


assert longest("ihgpwlah") == 370
assert longest("kglvqrro") == 492
assert longest("ulqzkmiv") == 830
print("Part 2:", longest(ipt_puzzle))

# Part 1 solution: RDRDUDLRDR
# Part 2 solution: 386
