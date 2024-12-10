ipt_36_81 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

ipt = ipt_36_81.split("\n")
ipt = open("input.txt").read().split("\n")


world = {}
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        if c != ".":
            world[complex(x, y)] = int(c)
dzs = [complex(0, 1) ** i for i in range(4)]

counts: dict[complex, list] = {}


def climb(z0, world, z, h):
    if h == 9 and world[z] == 9:
        counts[z0].append(z)
    else:
        for d in dzs:
            if (z + d in world) and (world[z + d] == h + 1):
                climb(z0, world, z + d, h + 1)


for z0 in world.keys():
    if world[z0] == 0:
        counts[z0] = []
        climb(z0, world, z0, 0)


r1 = sum([len(set(v)) for v in counts.values()])
r2 = sum([len(v) for v in counts.values()])

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 796
# Part 2 solution: 1942
