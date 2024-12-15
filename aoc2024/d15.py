# Input

ipt = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""".split(
    "\n\n"
)

ipt = open("input.txt").read().split("\n\n")


# Helpers


def print_field_complex(field, z_robot, x_min, x_max, y_min, y_max):
    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            z = complex(xx, yy)
            if z in field:
                ss += str(field[complex(xx, yy)])
            elif z == z_robot:
                ss += "@"
            else:
                ss += " "
        print(ss)


def create_world_complex(input):
    x_min, x_max, y_min, y_max = 0, len(input[0]), 0, len(input)
    field = {}
    z0_robot = 0
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            z = complex(x, y)
            if c == "#" or c == "O":
                field[z] = c
            if c == "@":
                z0_robot = z

    dirs4 = [complex(0, 1) ** i for i in range(4)]
    return field, x_min, x_max, y_min, y_max, dirs4, z0_robot


def create_world_complex_part2(input):
    x_min, x_max, y_min, y_max = 0, len(input[0]) * 2, 0, len(input)
    field = {}
    z0_robot = 0
    y = -1
    for line in input:
        y += 1
        x = -1
        for c in line:
            x += 1
            z = complex(x, y)
            if c == "#":
                field[z] = c
                field[z + 1] = c
            if c == "O":
                field[z] = "["
                field[z + 1] = "]"
            if c == "@":
                z0_robot = z
            x += 1

    dirs4 = [complex(0, 1) ** i for i in range(4)]

    return field, x_min, x_max, y_min, y_max, dirs4, z0_robot


def parse_moves(rules, dirs4):
    ret = []
    for d in rules:
        if d == ">":
            ret.append(dirs4[0])
        elif d == "v":
            ret.append(dirs4[1])
        elif d == "<":
            ret.append(dirs4[2])
        elif d == "^":
            ret.append(dirs4[3])
    return ret


def is_free(world, z):
    return z not in world


def is_wall(world, z):
    return z in world and world[z] == "#"


def is_box(world, z):
    return z in world and world[z] == "O"


# Part 1

world, x_min, x_max, y_min, y_max, dirs4, z0_robot = create_world_complex(
    ipt[0].split("\n")
)
moves = parse_moves(ipt[1], dirs4)

z_robot = z0_robot

for dz in moves:
    if is_free(world, z_robot + dz):
        z_robot += dz

    elif is_wall(world, z_robot + dz):
        pass

    elif is_box(world, z_robot + dz):
        k = 1
        while is_box(world, z_robot + k * dz):
            k += 1
        if is_free(world, z_robot + k * dz):
            del world[z_robot + dz]
            world[z_robot + k * dz] = "O"
            z_robot += dz

    # print_field_complex(world,z_robot,x_min, x_max, y_min, y_max)
    # input("Press any key")

r1 = sum([100 * int(z.imag) + int(z.real) for z in world.keys() if is_box(world, z)])


print(f"# Part 1 solution: {r1}")


# part 2 specific helpers


def is_anybox(world, z):
    return z in world and (world[z] == "[" or world[z] == "]")


def is_leftsideofbox(world, z):
    return z in world and (world[z] == "[")


def is_rightsideofbox(world, z):
    return z in world and (world[z] == "]")


def is_movable(world, z0, dz, to_move):
    if is_leftsideofbox(world, z0):
        if is_free(world, z0 + dz) and is_free(world, z0 + 1 + dz):
            to_move.add((z0, z0 + 1))
            return True, to_move
        elif is_anybox(world, z0 + dz) and is_anybox(world, z0 + 1 + dz):
            im1, l1 = is_movable(world, z0 + dz, dz, to_move)
            im2, l2 = is_movable(world, z0 + 1 + dz, dz, to_move)
            if im1 and im2:
                for e1 in l1:
                    to_move.add(e1)
                for e2 in l2:
                    to_move.add(e2)
                to_move.add((z0, z0 + 1))
                return True, to_move
        elif is_free(world, z0 + dz) and is_anybox(world, z0 + 1 + dz):
            im2, l2 = is_movable(world, z0 + 1 + dz, dz, to_move)
            if im2:
                for e2 in l2:
                    to_move.add(e2)
                to_move.add((z0, z0 + 1))
                return True, to_move
        elif is_anybox(world, z0 + dz) and is_free(world, z0 + 1 + dz):
            im1, l1 = is_movable(world, z0 + dz, dz, to_move)
            if im1:
                for e1 in l1:
                    to_move.add(e1)

                to_move.add((z0, z0 + 1))
                return True, to_move

        return False, to_move

    if is_rightsideofbox(world, z0):
        if is_free(world, z0 + dz) and is_free(world, z0 - 1 + dz):
            to_move.add((z0 - 1, z0))
            return True, to_move
        elif is_anybox(world, z0 + dz) and is_anybox(world, z0 - 1 + dz):
            im1, l1 = is_movable(world, z0 + dz, dz, to_move)
            im2, l2 = is_movable(world, z0 - 1 + dz, dz, to_move)
            if im1 and im2:
                for e1 in l1:
                    to_move.add(e1)
                for e2 in l2:
                    to_move.add(e2)
                to_move.add((z0 - 1, z0))
                return True, to_move
        elif is_free(world, z0 + dz) and is_anybox(world, z0 - 1 + dz):
            im2, l2 = is_movable(world, z0 - 1 + dz, dz, to_move)
            if im2:
                for e2 in l2:
                    to_move.add(e2)
                to_move.add((z0 - 1, z0))
                return True, to_move
        elif is_anybox(world, z0 + dz) and is_free(world, z0 - 1 + dz):
            im1, l1 = is_movable(world, z0 + dz, dz, to_move)

            if im1:
                for e1 in l1:
                    to_move.add(e1)

                to_move.add((z0 - 1, z0))
                return True, to_move
        return False, to_move
    quit("should not be here")
    return False, to_move


# Part 2

world, x_min, x_max, y_min, y_max, dirs4, z0_robot = create_world_complex_part2(
    ipt[0].split("\n")
)

z_robot = z0_robot


for dz in moves:

    if is_free(world, z_robot + dz):
        z_robot += dz

    elif is_wall(world, z_robot + dz):
        pass

    elif dz == 1:
        if is_leftsideofbox(world, z_robot + dz):
            k = 1
            while is_anybox(world, z_robot + k * dz):
                k += 1
            if is_free(world, z_robot + k * dz):
                del world[z_robot + dz]
                for i in range(1, k, 2):
                    world[z_robot + dz * i + 1] = "["
                    world[z_robot + dz * i + 2] = "]"
                z_robot += dz

    elif dz == -1:
        if is_rightsideofbox(world, z_robot + dz):
            k = 1
            while is_anybox(world, z_robot + k * dz):
                k += 1
            if is_free(world, z_robot + k * dz):
                del world[z_robot + dz]
                for i in range(1, k, 2):
                    world[z_robot + dz * i - 1] = "]"
                    world[z_robot + dz * i - 2] = "["
                z_robot += dz

    elif dz == 1j or dz == -1j:
        if is_anybox(world, z_robot + dz):
            to_move: set[tuple] = set()
            ok, to_move = is_movable(world, z_robot + dz, dz, to_move)
            if ok:
                to_place = set()
                for box in to_move:
                    to_place.add((box[0] + dz, box[1] + dz))
                for box in to_move:
                    if box[0] in world:
                        del world[box[0]]
                    if box[1] in world:
                        del world[box[1]]
                for box in to_place:
                    world[box[0]] = "["
                    world[box[1]] = "]"
                z_robot += dz

    # print_field_complex(world,z_robot,x_min, x_max, y_min, y_max)
    # input("Press any key")


r2 = sum(
    [
        100 * int(z.imag) + int(z.real)
        for z in world.keys()
        if is_leftsideofbox(world, z)
    ]
)


print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1563092
# Part 2 solution: 1582688
