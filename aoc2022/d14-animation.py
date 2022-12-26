# coding: utf-8
import os
import re

import imageio
import numpy as np
from boilerplate import read_input_file, run_func
from PIL import Image


def print_field(xyids, filenames, DBG=True):
    data = np.full((200, 200, 3), 0xCB, dtype=np.uint8)

    for yy in range(0, 200 + 1):
        for xx in range(400, 600 + 1):
            if (xx, yy) in xyids:
                if (xx - 400) >= 0 and (xx - 400) < 200:
                    if xyids[(xx, yy)] == "#":
                        data[yy, xx - 400] = [0x4C, 0x6A, 0xEF]
                    elif xyids[(xx, yy)] == "o":
                        data[yy, xx - 400] = [0xCD, 0xFA, 0x50]

    img = Image.fromarray(data)
    img = img.resize((600, 600), Image.Resampling.NEAREST)

    idx = len(filenames) + 1
    filename = f"{idx}.png"
    filenames.append(filename)

    # save frame
    img.save("tmp/" + filename, "PNG")


def make_world(input_val):
    field = {}
    max_y = 0
    for line in input_val:
        ii = list(map(int, re.findall(r"-?\d+", line)))
        idx = 0
        while idx + 4 <= len(ii):
            (x0, y0) = (ii[idx + 0], ii[idx + 1])
            (x1, y1) = (ii[idx + 2], ii[idx + 3])
            max_y = max(max_y, y0, y1)
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    field[(x0, y)] = "#"
            elif y0 == y1:
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    field[(x, y0)] = "#"
            idx += 2
    return field, max_y


def update_field(field, cur_x, cur_y, dx, dy):
    del field[(cur_x, cur_y)]
    (cur_x, cur_y) = (cur_x + dx, cur_y + dy)
    field[(cur_x, cur_y)] = "o"
    return (cur_x, cur_y)


def fall_new_grain(field, max_y):
    (cur_x, cur_y) = (500, 0)
    field[(cur_x, cur_y)] = "o"

    while cur_y <= max_y:
        if not (cur_x, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 0, 1)
        elif not (cur_x - 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, -1, 1)
        elif not (cur_x + 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 1, 1)
        else:
            return True
    # grain falls out
    del field[(cur_x, cur_y)]
    return False


def fall_new_grain2(field, max_y):
    (cur_x, cur_y) = (500, 0)
    field[(cur_x, cur_y)] = "#"

    while cur_y <= max_y:
        if not (cur_x, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 0, 1)
        elif not (cur_x - 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, -1, 1)
        elif not (cur_x + 1, cur_y + 1) in field:
            (cur_x, cur_y) = update_field(field, cur_x, cur_y, 1, 1)
        else:
            return cur_y > 0

    # grain of sand never falls out
    return True


def boom_part1(input_val, DBG=True):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    filenames = []
    field, max_y = make_world(input_val)
    step = 0

    while True:
        grain_stays_in = fall_new_grain(field, max_y)
        print_field(field, filenames, False)
        if not grain_stays_in:
            break
        step += 1
        if step % 10 == 0:
            print(str(step))

    # build gif
    print("d14p1 gif")
    images = list(map(lambda filename: imageio.v2.imread("tmp/" + filename), filenames))
    imageio.mimsave(os.path.join("d14p1.gif"), images, fps=30, loop=1)
    # Remove files
    for filename in set(filenames):
        os.remove("tmp/" + filename)

    return step


def boom_part2(input_val, DBG=True):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    filenames = []
    field, max_y = make_world(input_val)
    nb_grains = 0

    while True:
        grain_falls = fall_new_grain2(field, max_y)
        nb_grains += 1
        if nb_grains < 100:
            print_field(field, filenames, False)
        elif nb_grains < 1000 and nb_grains % 10 == 0:
            print_field(field, filenames, False)
        elif nb_grains < 10000 and nb_grains % 100 == 0:
            print_field(field, filenames, False)
        elif nb_grains < 100000 and nb_grains % 1000 == 0:
            print_field(field, filenames, False)

        if not grain_falls:
            break

        if nb_grains % 100 == 0:
            print(str(nb_grains))

    # build gif
    print("d14p2 gif")

    images = list(map(lambda filename: imageio.v2.imread("tmp/" + filename), filenames))
    imageio.mimsave(os.path.join("d14p2.gif"), images, fps=30, loop=1)
    # Remove files
    for filename in set(filenames):
        os.remove("tmp/" + filename)
    return nb_grains


puzzle_input = read_input_file("input-d14.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)
