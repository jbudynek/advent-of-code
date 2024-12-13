ipt140 = """AAAA
BBCD
BBCC
EEEC""".split(
    "\n"
)

ipt772 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""".split(
    "\n"
)

ipt1930_1206 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".split(
    "\n"
)

ipt2_368 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""".split(
    "\n"
)

ipt2_236 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""".split(
    "\n"
)

ipt2_80 = """AAAA
BBCD
BBCC
EEEC""".split(
    "\n"
)


ipt = ipt2_368
ipt = open("input.txt").read().split("\n")


dz4s = [complex(0, 1) ** i for i in range(4)]


world = {}
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        z = complex(x, y)
        world[z] = c

r1, r2 = 0, 0
done_area = set()
done_perim = set()
done_corners = set()


def area(z, v):
    a = 1
    done_area.add(z)
    for dz in dz4s:
        if z + dz in world and world[z + dz] == v and z + dz not in done_area:
            a += area(z + dz, v)
    return a


def perimeter(z, v):
    perim = 4
    done_perim.add(z)
    for dz in dz4s:
        if z + dz in world and world[z + dz] == v:
            perim = perim - 1
        if z + dz in world and world[z + dz] == v and z + dz not in done_perim:
            perim += perimeter(z + dz, v)
    return perim


corners_dict = {}


def corners(z0, z, v):
    if z0 not in corners_dict:
        corners_dict[z0] = {}

    square_corners = [0, 1, 1j, 1 + 1j]

    for dz in square_corners:
        sq_corner = z + dz
        if sq_corner not in corners_dict[z0]:
            corners_dict[z0][sq_corner] = 0
        corners_dict[z0][sq_corner] += 1

    done_corners.add(z)
    for dz in dz4s:
        if z + dz in world and world[z + dz] == v and z + dz not in done_corners:
            corners(z0, z + dz, v)


for z, val in world.items():
    ret_area, ret_perim, ret_corners = 0, 0, 0
    if z not in done_area:
        ret_area = area(z, val)
    if z not in done_perim:
        ret_perim = perimeter(z, val)
    if z not in done_corners:
        corners(z, z, val)
        for z_corner in corners_dict[z]:
            if corners_dict[z][z_corner] % 2 == 1:
                ret_corners += 1
            if corners_dict[z][z_corner] == 2:
                st = ""
                around = [0, 1, 1j, 1 + 1j]
                for i in range(len(around)):
                    around[i] += -1 - 1j
                for i, d in enumerate(around):
                    if z_corner + d in world:
                        st += world[z_corner + d]
                    else:
                        st += " "
                if (
                    (st[0] == val)
                    and (st[3] == val)
                    and (st[1] != val)
                    and (st[2] != val)
                ):
                    ret_corners += 2
                elif (
                    (st[1] == val)
                    and (st[2] == val)
                    and (st[0] != val)
                    and (st[3] != val)
                ):
                    ret_corners += 2

    r1 += ret_area * ret_perim
    r2 += ret_area * ret_corners


print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1452678
# Part 2 solution: 873584
