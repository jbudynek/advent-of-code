# coding: utf-8
import re
import sys

from boilerplate import read_input_file, run_func, test_func


def get_bounds(tracks, DBG):
    coords = tracks.keys()
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]
    return (x_min, x_max, y_min, y_max)


def parse_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == " ":
                continue
            else:
                field[(x, y)] = c

    if DBG:
        print(field)

    return field


def wrap_field(field, DBG):
    (x_min, x_max, y_min, y_max) = get_bounds(field, DBG)
    wrap_y = {}
    for y in range(y_min, y_max + 1):
        const_y = {}
        for x in range(x_min, x_max + 1):
            if (x, y) in field:
                const_y[(x, y)] = "#"
        xx_min = min(const_y, key=lambda t: t[0])[0]
        xx_max = max(const_y, key=lambda t: t[0])[0]
        wrap_y[y] = (xx_min, xx_max)

    wrap_x = {}
    for x in range(x_min, x_max + 1):
        const_x = {}
        for y in range(y_min, y_max + 1):
            if (x, y) in field:
                const_x[(x, y)] = "#"
        yy_min = min(const_x, key=lambda t: t[1])[1]
        yy_max = max(const_x, key=lambda t: t[1])[1]
        wrap_x[x] = (yy_min, yy_max)

    return wrap_x, wrap_y


def parse_path(ipt, DBG):
    dist = list(map(int, re.findall(r"-?\d+", ipt)))
    lr = list(map(str, re.findall(r"[LR]", ipt)))
    if DBG:
        print(dist, lr)
    return dist, lr


def apply_part1(field, x, y, facing, wrap_x, wrap_y, dist, lr):

    facing2dir = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }
    dir = facing2dir[facing]

    # first move n steps

    for _ in range(dist):
        nx = x + dir[0]
        ny = y + dir[1]

        # if we are out of the sides, wrap around
        if facing == "R":
            if (nx, ny) not in field:
                nx = wrap_y[ny][0]
        elif facing == "L":
            if (nx, ny) not in field:
                nx = wrap_y[ny][1]
        if facing == "U":
            if (nx, ny) not in field:
                ny = wrap_x[nx][1]
        elif facing == "D":
            if (nx, ny) not in field:
                ny = wrap_x[nx][0]

        if (nx, ny) in field and field[(nx, ny)] == "#":
            break
        else:
            x = nx
            y = ny

    # then, change orientation
    orientations_ccw = ["R", "D", "L", "U"]
    idx = orientations_ccw.index(facing)
    if lr == "X":
        nfacing = facing
    elif lr == "R":
        nfacing = orientations_ccw[(idx + 1) % 4]
    elif lr == "L":
        nfacing = orientations_ccw[(idx - 1) % 4]
    else:
        print("error")
        sys.exit()

    return x, y, nfacing


def print_field_and_position(xyids, x, y, f, DBG=True):
    coords = xyids.keys()
    x_min = min(coords, key=lambda t: t[0])[0] - 1
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1] - 1
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if x == xx and y == yy:
                if f == "U":
                    ss += "^"
                elif f == "D":
                    ss += "v"
                elif f == "L":
                    ss += "<"
                elif f == "R":
                    ss += ">"
            elif (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)


def increment_position_part2(x, y, facing):
    # sides position in real data:
    # .12
    # .3.
    # 45.
    # 6..

    if facing == "R":
        # 2 to 5
        if 0 <= y < 50 and x == 150:
            facing = "L"
            (x, y) = (99, 149 - y)
        # 3 to 2
        elif 50 <= y < 100 and x == 100:
            facing = "U"
            (x, y) = (y + 50, 49)
        # 5 to 2
        elif 100 <= y < 150 and x == 100:
            facing = "L"
            (x, y) = (149, 149 - y)
        # 6 to 5
        elif 150 <= y < 200 and x == 50:
            facing = "U"
            (x, y) = (y - 100, 149)
    elif facing == "L":
        # 1 to 4
        if 0 <= y < 50 and x == 49:
            facing = "R"
            (x, y) = (0, 149 - y)
        # 3 to 4
        elif 50 <= y < 100 and x == 49:
            facing = "D"
            (x, y) = (y - 50, 100)
        # 4 to 1
        elif 100 <= y < 150 and x == -1:
            facing = "R"
            (x, y) = (50, 149 - y)
        # 6 to 1
        elif 150 <= y < 200 and x == -1:
            facing = "D"
            (x, y) = (y - 100, 0)
    elif facing == "D":
        # 2 to 3
        if 100 <= x < 150 and y == 50:
            facing = "L"
            (x, y) = (99, x - 50)
        # 5 to 6
        elif 50 <= x < 100 and y == 150:
            facing = "L"
            (x, y) = (49, x + 100)
        # 6 to 2
        elif 0 <= x < 50 and y == 200:
            (x, y) = (x + 100, 0)
    elif facing == "U":
        # 2 to 6
        if 100 <= x < 150 and y == -1:
            (x, y) = (x - 100, 199)
        # 1 to 6
        elif 50 <= x < 100 and y == -1:
            facing = "R"
            (x, y) = (0, x + 100)
        # 4 to 3
        elif 0 <= x < 50 and y == 99:
            facing = "R"
            (x, y) = (50, x + 50)

    return x, y, facing


##############


def apply_part2(field, x, y, facing, dist, lr):

    # sides are organized like that in real data
    # .12
    # .3.
    # 45.
    # 6..

    facing2dir = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    # first, move n steps
    for _ in range(dist):
        dir = facing2dir[facing]
        nx = x + dir[0]
        ny = y + dir[1]
        nfacing = facing
        if (nx, ny) not in field:
            # got out of side, see what side we land on
            nx, ny, nfacing = increment_position_part2(nx, ny, facing)
        if (nx, ny) in field and field[(nx, ny)] == "#":
            # hit wall, break out of loop
            break
        else:
            x = nx
            y = ny
            facing = nfacing

    # then, change orientation
    orientations_ccw = ["R", "D", "L", "U"]
    idx = orientations_ccw.index(facing)
    if lr == "X":
        nfacing = facing
    elif lr == "R":
        nfacing = orientations_ccw[(idx + 1) % 4]
    elif lr == "L":
        nfacing = orientations_ccw[(idx - 1) % 4]
    else:
        print("error")
        sys.exit()

    return x, y, nfacing


#############


def boom_part1(input_val, DBG=True):
    field = parse_world(input_val[:-2], DBG)
    if DBG:
        print_field_and_position(field, -1, -1, DBG)
    wrap_x, wrap_y = wrap_field(field, DBG)

    dist, lr = parse_path(input_val[-1], DBG)

    (x, y) = (wrap_y[0][0], 0)

    facing = "R"
    if DBG:
        print("start", x, y, facing)
    lr.append("X")
    for i in range(len(dist)):
        if DBG:
            print("** move", i, ":", dist[i], lr[i])

        (nx, ny, nfacing) = apply_part1(
            field, x, y, facing, wrap_x, wrap_y, dist[i], lr[i]
        )

        if DBG:
            print("pos ", nx, ny, nfacing)
        x = nx
        y = ny
        facing = nfacing

        if DBG:
            print_field_and_position(field, x, y, facing, DBG)

    if DBG:
        print("last pos ", x, y, facing)

    ret = 1000 * (y + 1) + 4 * (x + 1)

    if facing == "L":
        ret += 2
    elif facing == "R":
        ret += 0
    if facing == "D":
        ret += 1
    if facing == "U":
        ret += 3

    return ret


def boom_part2(input_val, DBG=True):

    field = parse_world(input_val[:-2], DBG)
    if DBG:
        print_field_and_position(field, -1, -1, DBG)

    ii, lr = parse_path(input_val[-1], DBG)

    (x, y) = (50, 0)

    facing = "R"
    if DBG:
        print("start", x, y, facing)
    lr.append("X")

    for i in range(len(ii)):
        if DBG:
            print("** move", i, ":", ii[i], lr[i])

        (nx, ny, nfacing) = apply_part2(field, x, y, facing, ii[i], lr[i])

        if DBG:
            print("pos ", nx, ny, nfacing)
        x = nx
        y = ny
        facing = nfacing

        if DBG:
            print_field_and_position(field, x, y, facing, DBG)

    if DBG:
        print("last pos ", x, y, facing)

    ret = 1000 * (y + 1) + 4 * (x + 1)

    if facing == "L":
        ret += 2
    elif facing == "R":
        ret += 0
    if facing == "D":
        ret += 1
    if facing == "U":
        ret += 3

    return ret


# Test cases
##########

t1 = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 6032, True)
# sys.exit()

# Part 2 is hardcoded to real data, so code for part 2 does not work with test data
# test_func(boom_part2, tt1, 5031, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d22.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

sys.exit()

# PART 1 OK = 13566
# PART 2 OK = 11451
