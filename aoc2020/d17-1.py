# coding: utf-8
import sys
import time
from itertools import product

# for this puzzle we use a dict indexed by (x,y) for each slice,
# and a dict indexed by z to store the slices.
# as we will see in part 2, it is not the best idea but it works.


def print_world(world):
    for (k, v) in world.items():
        print("z=", k)
        print_one_slice(v)


def print_one_slice(xyids, DBG=True):

    coords = xyids.keys()
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                ss += xyids[(xx, yy)]
            else:
                ss += " "
        print(ss)


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == ".":
                continue
            elif c == "#":
                field[(x, y)] = c
            else:
                print("panic")
                sys.exit()

    if DBG:
        print(field)
    if DBG:
        print_one_slice(field, DBG)

    coords = field.keys()
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0]
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1]
    return (field, x_min, x_max, y_min, y_max)


def get_world_bounds(world):
    z_min = 0
    z_max = 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    for (k, v) in world.items():
        z_min = min(k, z_min)
        z_max = max(k, z_max)
        coords = v.keys()
        x_min = min(x_min, min(coords, key=lambda t: t[0])[0])
        x_max = max(x_max, max(coords, key=lambda t: t[0])[0])
        y_min = min(y_min, min(coords, key=lambda t: t[1])[1])
        y_max = max(y_max, max(coords, key=lambda t: t[1])[1])

    return (x_min, x_max, y_min, y_max, z_min, z_max)


def is_active(world, x, y, z):
    return z in world and (x, y) in world[z]


def set_active(new_world, x, y, z):
    if z not in new_world:
        new_world[z] = {}
    if (x, y) not in new_world[z]:
        new_world[z][(x, y)] = "#"


def set_inactive(new_world, x, y, z):
    if z not in new_world:
        return
    if (x, y) in new_world[z]:
        del new_world[z][(x, y)]
    if len(new_world[z]) == 0:
        del new_world[z]


def neighbors(world, x, y, z):
    n = 0
    for (dx, dy, dz) in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
        if (dx, dy, dz) == (0, 0, 0):
            continue
        if z + dz in world and (x + dx, y + dy) in world[z + dz]:
            n = n + 1
    return n


def count_cubes(world):
    ret = 0
    for slice in world.values():
        ret = ret + len(slice)
    return ret


def tick(world, x_min, x_max, y_min, y_max, z_min, z_max, DBG=True):

    new_world = {}
    for z in range(z_min - 1, z_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for x in range(x_min - 1, x_max + 2):
                n = neighbors(world, x, y, z)
                a = is_active(world, x, y, z)
                if a:
                    if n == 2 or n == 3:
                        set_active(new_world, x, y, z)
                    else:
                        set_inactive(new_world, x, y, z)
                elif not a:
                    if n == 3:
                        set_active(new_world, x, y, z)
                    else:
                        set_inactive(new_world, x, y, z)

    (x_min, x_max, y_min, y_max, z_min, z_max) = get_world_bounds(new_world)
    return (new_world, x_min, x_max, y_min, y_max, z_min, z_max)


def boom(input_val, DBG=True):

    # parse world
    (field, x_min, x_max, y_min, y_max) = create_world(input_val, DBG)

    world = {}
    world[0] = field
    z_min = 0
    z_max = 0

    max_tick = 6

    t = 0
    if DBG:
        print("tick=", t)
        print_world(world)

    count = 0

    while True:
        t = t + 1
        (
            new_world,
            new_x_min,
            new_x_max,
            new_y_min,
            new_y_max,
            new_z_min,
            new_z_max,
        ) = tick(world, x_min, x_max, y_min, y_max, z_min, z_max, DBG)
        world = new_world
        x_min = new_x_min
        x_max = new_x_max
        y_min = new_y_min
        y_max = new_y_max
        z_min = new_z_min
        z_max = new_z_max

        count_new = count_cubes(world)

        if DBG:
            print("tick=", t, "count=", count_new)

        count = count_new
        if t == max_tick:
            if DBG:
                print("***TICK", t, "***", count)
            break

    ret = count

    return ret


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


t1 = """.#.
..#
###"""
tt1 = t1.splitlines()
test(tt1, 112, True)
# sys.exit()

INPUT_FILE = "input-d17.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 1 = 202
