# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: direct simulation of the combat, following the rules literally.
# - Units are kept as [y, x, kind, hp]; each round they act in reading order
#   (sorted by (y, x) at the start of the round), skipping the ones killed
#   earlier in the round.
# - On its turn a unit looks for enemies; none left -> combat ends (the round
#   is not counted as complete).
# - If no enemy is adjacent, it moves: a BFS from the unit gives the distance
#   to every reachable open square; among the squares adjacent to enemies we
#   keep the nearest one, ties broken by reading order. Then a second BFS
#   from that chosen square gives distances to it, and the unit steps to the
#   adjacent open square with the smallest distance (ties: reading order).
# - Then it attacks the adjacent enemy with the fewest HP (ties: reading order).
# - Outcome = full rounds * sum of remaining HP.

# Part 2: same simulation, parameterised by the Elves' attack power. Starting
# at 4, we re-run the whole combat with increasing power until a run ends
# with no Elf dead (runs are aborted at the first Elf death to save time).
# The outcome of that first flawless run is the answer.

from collections import deque

ipt_test = [
    (
        """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""",
        27730,
    ),
    (
        """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""",
        36334,
    ),
    (
        """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
        39514,
    ),
    (
        """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
        27755,
    ),
    (
        """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""",
        28944,
    ),
    (
        """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""",
        18740,
    ),
]
ipt_puzzle = open("input.txt").read().strip()

DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # reading order


def parse(s):
    walls = set()
    units = []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((y, x))
            elif c in "EG":
                units.append([y, x, c, 200])
    return walls, units


def bfs(start, blocked):
    dist = {start: 0}
    q = deque([start])
    while q:
        y, x = q.popleft()
        for dy, dx in DIRS:
            n = (y + dy, x + dx)
            if n not in dist and n not in blocked:
                dist[n] = dist[(y, x)] + 1
                q.append(n)
    return dist


def combat(s, elf_power=3, stop_on_elf_death=False):
    # returns (outcome, True if no Elf died); with stop_on_elf_death the
    # combat is abandoned at the first Elf death (outcome is then None)
    walls, units = parse(s)
    rounds = 0
    while True:
        units.sort(key=lambda u: (u[0], u[1]))
        for u in units:
            if u[3] <= 0:
                continue
            enemies = [e for e in units if e[3] > 0 and e[2] != u[2]]
            if not enemies:
                elves_ok = all(v[3] > 0 for v in units if v[2] == "E")
                return rounds * sum(v[3] for v in units if v[3] > 0), elves_ok
            occupied = {(v[0], v[1]) for v in units if v[3] > 0}
            epos = {(e[0], e[1]) for e in enemies}

            def adjacent_enemies():
                return [
                    e
                    for e in enemies
                    if e[3] > 0 and abs(e[0] - u[0]) + abs(e[1] - u[1]) == 1
                ]

            if not adjacent_enemies():
                blocked = walls | occupied
                blocked.discard((u[0], u[1]))
                dist = bfs((u[0], u[1]), blocked)
                in_range = {
                    (y + dy, x + dx)
                    for (y, x) in epos
                    for dy, dx in DIRS
                    if (y + dy, x + dx) in dist
                }
                if in_range:
                    target = min(in_range, key=lambda p: (dist[p], p))
                    back = bfs(target, blocked)
                    steps = [
                        (u[0] + dy, u[1] + dx)
                        for dy, dx in DIRS
                        if (u[0] + dy, u[1] + dx) in back
                    ]
                    u[0], u[1] = min(steps, key=lambda p: (back[p], p))
            adj = adjacent_enemies()
            if adj:
                t = min(adj, key=lambda e: (e[3], e[0], e[1]))
                t[3] -= elf_power if u[2] == "E" else 3
                if stop_on_elf_death and t[2] == "E" and t[3] <= 0:
                    return None, False
        units = [v for v in units if v[3] > 0]
        rounds += 1


def part1(s):
    return combat(s)[0]


def part2(s):
    power = 4
    while True:
        outcome, ok = combat(s, power, stop_on_elf_death=True)
        if ok:
            return outcome
        power += 1


for t, expected in ipt_test:
    assert part1(t) == expected, (part1(t), expected)

# expected part 2 outcomes (None: example without a given answer)
for (t, _), expected in zip(ipt_test, [4988, None, 31284, 3478, 6474, 1140]):
    if expected is not None:
        assert part2(t) == expected, (part2(t), expected)

print("Part 1:", part1(ipt_puzzle))
print("Part 2:", part2(ipt_puzzle))

# Part 1 solution: 190012
# Part 2 solution: 34364
