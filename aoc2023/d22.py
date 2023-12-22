# coding: utf-8
import re

import numpy as np
from boilerplate import read_input_file, run_func, test_func

# Algorithm:
# store 2 dicts:
# brick id to (xyz) position (this changes)
# brick id to (dx dy dz) size (this does not change)
# and store the world: map (xyz) to brick id - this is sparse (hopefully)

# to fall, here is how you do it (the tetris part):
# sort the brick ids by z position of the brick (see np.argsort it's great)
# (from lowest - closest to z=1 - to highest)
# iterate in that order over bricks
# test if there is free space below
# if yes, move it down and re-sort the ids since positions have changed
# when there is no free space left, restart at lowest brick
# when you hit the last (highest) brick and it cannot move, you're done

# then you want to see what happens when you remove one brick (the djenga part)
# iterate on bricks (order doesn't matter)
# copy your world and maps, remove the brick
# (in practice you move it below z=0 in its entirety)
# test if any other brick has space below
# if yes:
# for part 1 you just have to remember that
# part 2 you need to run the falling algo described earlier
# and store the id of bricks that move (put them in a set)
# takes a little while, works fine.


def parse_ipt(ipt):
    world = {}
    brick2pos = []
    brick2size = {}
    for i, line in enumerate(ipt):
        ii = list(map(int, re.findall(r"-?\d+", line)))

        brick2pos.append((ii[0], ii[1], ii[2]))
        brick2size[i] = (ii[3] - ii[0], ii[4] - ii[1], ii[5] - ii[2])
        for x in range(ii[0], ii[3] + 1):
            for y in range(ii[1], ii[4] + 1):
                for z in range(ii[2], ii[5] + 1):
                    world[(x, y, z)] = i
    return world, brick2pos, brick2size


def is_free_below(i, world, brick2pos, brick2size):
    (x, y, z) = brick2pos[i]
    (dx, dy, _) = brick2size[i]
    if z <= 1:
        return False
    for xx in range(x, x + dx + 1):
        for yy in range(y, y + dy + 1):
            if (xx, yy, z - 1) in world:
                return False
    return True


def move_down(i, world, brick2pos, brick2size, moved):
    (x, y, z) = brick2pos[i]
    (dx, dy, dz) = brick2size[i]
    if z > 1:
        for xx in range(x, x + dx + 1):
            for yy in range(y, y + dy + 1):
                for zz in range(z, z + dz + 1):
                    del world[(xx, yy, zz)]
        brick2pos[i] = (x, y, z - 1)
        moved.add(i)
        for xx in range(x, x + dx + 1):
            for yy in range(y, y + dy + 1):
                for zz in range(z - 1, z - 1 + dz + 1):
                    world[(xx, yy, zz)] = i
    return world, brick2pos, brick2size, moved


def fall(world, brick2pos, brick2size, moved):
    arr = np.array(brick2pos, dtype=[("c1", int), ("c2", int), ("c3", int)])
    order = np.argsort(arr["c3"])
    idx = 0
    while idx < len(order):
        i = order[idx]
        while is_free_below(i, world, brick2pos, brick2size):
            move_down(i, world, brick2pos, brick2size, moved)
            arr = np.array(brick2pos, dtype=[("c1", int), ("c2", int), ("c3", int)])
            order = np.argsort(arr["c3"])
            idx = -1
        idx += 1
    return world, brick2pos, brick2size, moved


def remove_from_world(i, world, brick2pos, brick2size):
    world2 = world.copy()
    brick2pos2 = brick2pos.copy()

    (x, y, z) = brick2pos[i]
    (dx, dy, dz) = brick2size[i]
    for xx in range(x, x + dx + 1):
        for yy in range(y, y + dy + 1):
            for zz in range(z, z + dz + 1):
                del world2[(xx, yy, zz)]

    brick2pos2[i] = (x, y, -dz)
    return world2, brick2pos2, brick2size


def test_disintegration(world, brick2pos, brick2size, b_fall):

    arr = np.array(brick2pos, dtype=[("c1", int), ("c2", int), ("c3", int)])
    order = np.argsort(arr["c3"])

    idx = 0
    disintegrable = {}
    while idx < len(order):
        i = order[idx]
        world2, brick2pos2, brick2size = remove_from_world(
            i, world, brick2pos, brick2size
        )
        moved = set()
        for z in range(idx + 1, len(order)):
            test_i = order[z]
            if is_free_below(test_i, world2, brick2pos2, brick2size):
                if b_fall:
                    world2, brick2pos2, brick2size, moved = fall(
                        world2, brick2pos2, brick2size, moved
                    )
                disintegrable[i] = len(moved)
                break
        idx += 1
    return disintegrable, world, brick2pos, brick2size


def boom_part1(ipt, DBG=True):
    world, brick2pos, brick2size = parse_ipt(ipt)

    world, brick2pos, brick2size, _ = fall(world, brick2pos, brick2size, set())

    disintegrable, world, brick2pos, brick2size = test_disintegration(
        world, brick2pos, brick2size, False
    )

    ans = len(brick2pos) - len(disintegrable)

    return ans


def boom_part2(ipt, DBG=True):
    world, brick2pos, brick2size = parse_ipt(ipt)

    world, brick2pos, brick2size, _ = fall(world, brick2pos, brick2size, set())

    disintegrable, world, brick2pos, brick2size = test_disintegration(
        world, brick2pos, brick2size, True
    )

    ans = sum(disintegrable.values())

    return ans


# Test cases
#############


ipt_test1 = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".splitlines()
test_func(boom_part1, ipt_test1, 5, True)
test_func(boom_part2, ipt_test1, 7, True)

# Real data
############

ipt_puzzle = read_input_file("input-d22.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 432
# Part 2 solution: 63166
