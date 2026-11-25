# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# The grid has 128 rows; row i is the 128-bit knot hash of "<key>-<i>".
# Knot hash (not defined in the day 14 text, implemented from memory of day 10):
# - lengths = ASCII codes of the string + [17, 31, 73, 47, 23]
# - 64 rounds over a circular list 0..255 (position and skip size persist across
#   rounds): reverse the sublist of each length starting at the position, then
#   advance the position by length + skip and increment skip
# - dense hash: XOR each block of 16 numbers -> 16 bytes -> 32 hex digits
# - Part 1: convert each row's hex digits to bits and count the 1s (used squares).
# - Part 2: count regions, i.e. connected components of used squares (4-neighbour
#   adjacency, no diagonals). Scan the grid; each time an unvisited used square is
#   found, count a new region and flood-fill it (DFS with a stack) to mark all its
#   squares as visited.

ipt_test = "flqrgnkx"

ipt_puzzle = open("input.txt").read().strip()


def knot_hash(s):
    lengths = [ord(c) for c in s] + [17, 31, 73, 47, 23]
    nums = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
        for ln in lengths:
            idx = [(pos + i) % 256 for i in range(ln)]
            vals = [nums[i] for i in idx][::-1]
            for i, v in zip(idx, vals):
                nums[i] = v
            pos = (pos + ln + skip) % 256
            skip += 1
    dense = []
    for b in range(16):
        x = 0
        for v in nums[b * 16 : (b + 1) * 16]:
            x ^= v
        dense.append(x)
    return "".join(f"{x:02x}" for x in dense)


def grid(key):
    rows = []
    for i in range(128):
        h = knot_hash(f"{key}-{i}")
        rows.append("".join(f"{int(c, 16):04b}" for c in h))
    return rows


def used(key):
    return sum(row.count("1") for row in grid(key))


def regions(key):
    g = grid(key)
    seen = set()
    n = 0
    for r in range(128):
        for c in range(128):
            if g[r][c] == "1" and (r, c) not in seen:
                n += 1
                seen.add((r, c))
                stack = [(r, c)]
                while stack:
                    y, x = stack.pop()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if (
                            0 <= ny < 128
                            and 0 <= nx < 128
                            and g[ny][nx] == "1"
                            and (ny, nx) not in seen
                        ):
                            seen.add((ny, nx))
                            stack.append((ny, nx))
    return n


# test
r_test1 = used(ipt_test)
print(f"# Test part 1: {r_test1} (expected 8108)")
r_test2 = regions(ipt_test)
print(f"# Test part 2: {r_test2} (expected 1242)")
assert r_test1 == 8108
assert r_test2 == 1242

r1 = used(ipt_puzzle)
r2 = regions(ipt_puzzle)
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 8216
# Part 2 solution: 1139
