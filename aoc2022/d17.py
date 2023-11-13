# coding: utf-8
import sys

from boilerplate import read_input_file, run_func, test_func

BLOCKS = {
    "-": ["####"],
    "+": [".#.", "###", ".#."],
    "L": ["..#", "..#", "###"],
    "|": ["#", "#", "#", "#"],
    "o": ["##", "##"],
}

ORDER = ["-", "+", "L", "|", "o"]

W = 7
LE = 2
BE = 3


def test_free_left(field, cur_block, cur_x, cur_y):
    if cur_block == "-":
        if (cur_x - 1, cur_y) not in field:
            return True
        else:
            return False
    elif cur_block == "+":
        if (
            (cur_x, cur_y) not in field
            and (cur_x - 1, cur_y - 1) not in field
            and (cur_x, cur_y - 2) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "L":
        if (
            (cur_x + 1, cur_y) not in field
            and (cur_x + 1, cur_y - 1) not in field
            and (cur_x - 1, cur_y - 2) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "|":
        if (
            (cur_x - 1, cur_y) not in field
            and (cur_x - 1, cur_y - 1) not in field
            and (cur_x - 1, cur_y - 2) not in field
            and (cur_x - 1, cur_y - 3) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "o":
        if (cur_x - 1, cur_y) in field and not (cur_x - 1, cur_y - 1) not in field:
            return True
        else:
            return False
    else:
        print("BLOCK ERROR")
        sys.exit()
    return False


def test_free_right(field, cur_block, cur_x, cur_y):
    if cur_block == "-":
        if (cur_x + 4, cur_y) not in field:
            return True
        else:
            return False
    elif cur_block == "+":
        if (
            (cur_x + 2, cur_y) not in field
            and (cur_x + 3, cur_y - 1) not in field
            and (cur_x + 2, cur_y - 2) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "L":
        if (
            (cur_x + 3, cur_y) not in field
            and (cur_x + 3, cur_y - 1) not in field
            and (cur_x + 3, cur_y - 2) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "|":
        if (
            (cur_x + 1, cur_y) not in field
            and (cur_x + 1, cur_y - 1) not in field
            and (cur_x + 1, cur_y - 2) not in field
            and (cur_x + 1, cur_y - 3) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "o":
        if (cur_x + 2, cur_y) in field and not (cur_x + 2, cur_y - 1) not in field:
            return True
        else:
            return False
    else:
        print("BLOCK ERROR")
        sys.exit()
    return True


def test_free_down(field, cur_block, cur_x, cur_y):
    if cur_block == "-":
        if (
            (cur_x, cur_y - 1) not in field
            and (cur_x + 1, cur_y - 1) not in field
            and (cur_x + 2, cur_y - 1) not in field
            and (cur_x + 3, cur_y - 1) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "+":
        if (
            (cur_x, cur_y - 2) not in field
            and (cur_x + 1, cur_y - 3) not in field
            and (cur_x + 2, cur_y - 2) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "L":
        if (
            (cur_x, cur_y - 3) not in field
            and (cur_x + 1, cur_y - 3) not in field
            and (cur_x + 2, cur_y - 3) not in field
        ):
            return True
        else:
            return False
    elif cur_block == "|":
        if (cur_x, cur_y - 4) not in field:
            return True
        else:
            return False
    elif cur_block == "o":
        if (cur_x, cur_y - 2) in field and not (cur_x + 1, cur_y - 2) not in field:
            return True
        else:
            return False
    else:
        print("BLOCK ERROR")
        sys.exit()
    return True


def put_block(field, cur_block, cur_x, cur_y):
    for idx, line in enumerate(BLOCKS[cur_block]):
        for jdx, c in enumerate(line):
            if c == "#":
                field[(cur_x + jdx, cur_y - idx)] = "#"
    return cur_y


def boom_part1(input_val, DBG=True):

    field = {}

    for i in range(W):
        field[(i, 0)] = "#"

    top = 0
    max_top = 0

    nb_blocks = -1
    jdx = 0

    while True:
        nb_blocks += 1
        if nb_blocks == 2022:
            return max_top
        cur_block = ORDER[nb_blocks % len(ORDER)]
        h_block = len(BLOCKS[cur_block])

        cur_y = max_top + BE + h_block

        for i in range(BE + h_block):
            field[(-1, cur_y - i)] = "#"
            field[(W, cur_y - i)] = "#"

        cur_x = LE

        stop = False
        while not stop:
            cur_jet = input_val[jdx % len(input_val)]
            jdx += 1
            if cur_jet == "<":
                if test_free_left(field, cur_block, cur_x, cur_y):
                    cur_x -= 1
            elif cur_jet == ">":
                if test_free_right(field, cur_block, cur_x, cur_y):
                    cur_x += 1
            else:
                print("JET ERROR")
                sys.exit()
            if test_free_down(field, cur_block, cur_x, cur_y):
                cur_y -= 1
            else:
                top = put_block(field, cur_block, cur_x, cur_y)
                max_top = max(top, max_top)
                stop = True

    return max_top


def clear_field(field, maxy):
    keys = list(field.keys())
    for k in keys:
        if k[1] < maxy:
            del field[k]


def boom_part2(input_val, DBG=True):

    # find when jdx loops when we deal with first block

    field = {}

    for i in range(W):
        field[(i, 0)] = "#"

    top = 0
    max_top = 0

    nb_blocks = -1
    jdx = 0

    all_jdx = {}
    all_tops = {}

    nb_wind = len(input_val)

    while True:
        nb_blocks += 1

        key = jdx % nb_wind
        if nb_blocks % nb_wind == 0:
            if key in all_jdx:
                if DBG:
                    print(nb_blocks, jdx, key, max_top, all_jdx[key])
                nb0 = all_jdx[key]
                h0 = all_tops[nb0]
                len_loop = nb_blocks - nb0
                delta_h = max_top - h0
                after_loop = (1000000000000 - nb0) % len_loop
                nb_loops = (1000000000000 - nb0) // len_loop
                hh = delta_h * nb_loops + all_tops[nb0 + after_loop]
                return hh

            else:
                if DBG:
                    print(nb_blocks, jdx, key, max_top)
                all_jdx[key] = nb_blocks
        all_tops[nb_blocks] = max_top

        if nb_blocks == -1:
            return max_top
        cur_block = ORDER[nb_blocks % len(ORDER)]
        h_block = len(BLOCKS[cur_block])

        cur_y = max_top + BE + h_block

        for i in range(BE + h_block):
            field[(-1, cur_y - i)] = "#"
            field[(W, cur_y - i)] = "#"

        cur_x = LE

        stop = False

        while not stop:
            cur_jet = input_val[jdx % len(input_val)]

            jdx += 1
            if cur_jet == "<":
                if test_free_left(field, cur_block, cur_x, cur_y):
                    cur_x -= 1
            elif cur_jet == ">":
                if test_free_right(field, cur_block, cur_x, cur_y):
                    cur_x += 1
            else:
                print("JET ERROR")
                sys.exit()
            if test_free_down(field, cur_block, cur_x, cur_y):
                cur_y -= 1
            else:
                top = put_block(field, cur_block, cur_x, cur_y)
                max_top = max(top, max_top)
                # manual garbage collection...
                if nb_blocks % 10000 == 0:
                    clear_field(field, max_top - 1000)
                stop = True

    return max_top


# Test cases
##########


t1 = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
tt1 = t1.splitlines()
test_func(boom_part1, tt1[0], 3068, True)
test_func(boom_part2, tt1[0], 1514285714288, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d17.txt")[0]

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 3224
# PART 2 OK = 1595988538691
