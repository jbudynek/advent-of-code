# we read the input into a complex plane, which is a dict of characters indexed
# by complex numbers. This is the world. We prepare an array of eight complex
# numbers to get to the neighbors of a particular location.
# (note the one-liner for dzs)
# Part 1: iterate on keys of the world (each point in the complex plane).
# If it's an 'X', we look straight in the eight directions to see if 'XMAS' is
# written.
# Part 2: prepare a subset of the directions that goes only in the 4 corners.
# Iterate on keys of the world, if it's an 'A', look in the corners to see if
# we have 'MAS' or 'SAM'.


ipt_test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

# ipt = ipt_test.splitlines()
ipt = open("input.txt").read().splitlines()

world = {}
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        world[complex(x, y)] = c

dzs = [complex(1, 1) ** i / 2 ** (i // 2) for i in range(8)]

result1 = 0
for z0 in world.keys():
    if world[z0] != "X":
        continue
    for dz in dzs:
        mas = (
            world.get(z0 + dz, "")
            + world.get(z0 + 2 * dz, "")
            + world.get(z0 + 3 * dz, "")
        )
        if mas == "MAS":
            result1 += 1

result2 = 0
xx = dzs[1::2]
for z0 in world.keys():
    if world[z0] != "A":
        continue
    ms1 = world.get(z0 + xx[0], "") + world.get(z0 + xx[2], "")
    ms2 = world.get(z0 + xx[1], "") + world.get(z0 + xx[3], "")
    if ms1 in ("MS", "SM") and ms2 in ("MS", "SM"):
        result2 += 1

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 2549
# Part 2 solution: 2003
