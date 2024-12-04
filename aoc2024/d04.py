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
