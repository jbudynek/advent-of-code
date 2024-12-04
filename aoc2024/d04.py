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


def create_world_complex(lines):
    world = {}
    x, y = -1, -1
    for line in lines:
        y += 1
        x = -1
        for c in line:
            x += 1
            world[complex(x, y)] = c
    # 8 neighbors
    dz = [complex(1, 1) ** i / 2 ** (i // 2) for i in range(8)]
    return world, dz


world, dzs = create_world_complex(ipt)

result1 = 0
for z0 in world.keys():
    if world[z0] != "X":
        continue
    for dz in dzs:
        if z0 + 3 * dz not in world:
            continue
        mas = world[z0 + dz] + world[z0 + 2 * dz] + world[z0 + 3 * dz]
        if mas == "MAS":
            result1 += 1

result2 = 0
x = dzs[1::2]
for z0 in world.keys():
    if (
        world[z0] != "A"
        or z0 + x[0] not in world
        or z0 + x[1] not in world
        or z0 + x[2] not in world
        or z0 + x[3] not in world
    ):
        continue
    ms1 = world[z0 + x[0]] + world[z0 + x[2]]
    ms2 = world[z0 + x[1]] + world[z0 + x[3]]
    if ms1 in ("MS", "SM") and ms2 in ("MS", "SM"):
        result2 += 1

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 2549
# Part 2 solution: 2003
