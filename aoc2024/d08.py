ipt = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".splitlines()

ipt = open("input.txt").read().splitlines()

ants: dict[str, list[complex]] = {}
max_x, max_y = len(ipt[0]), len(ipt)
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        if c != ".":
            if c not in ants:
                ants[c] = []
            ants[c].append(complex(x, y))

nodes1, nodes2 = set(), set()


def inside(z):
    return z.real >= 0 and z.real < max_x and z.imag >= 0 and z.imag < max_y


for k in ants.keys():
    for i, z1 in enumerate(ants[k]):
        for j in range(i + 1, len(ants[k])):
            z2 = ants[k][j]
            dz = z2 - z1

            # part 1
            if inside(z1 - dz):
                nodes1.add(z1 - dz)
            if inside(z2 + dz):
                nodes1.add(z2 + dz)

            # part 2
            z0 = z1
            while inside(z0):
                nodes2.add(z0)
                z0 -= dz
            z0 = z2
            while inside(z0):
                nodes2.add(z0)
                z0 += dz

print(f"# Part 1 solution: {len(nodes1)}")
print(f"# Part 2 solution: {len(nodes2)}")

# Part 1 solution: 301
# Part 2 solution: 1019
