# coding: utf-8

import time


def function(ii, DBG=True):

    world = {}
    cur_x = 0
    cur_y = 0

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    cur_dir = 0

    delta_0 = 1
    delta_1 = 1
    last_turn = 0

    for i in range(1, ii):
        world[(cur_x, cur_y)] = i
        cur_x = cur_x + directions[cur_dir][0]
        cur_y = cur_y + directions[cur_dir][1]
        if i - last_turn == delta_0:
            cur_dir = (cur_dir + 1) % len(directions)
            last_turn = i
            if delta_0 == delta_1:
                delta_0 = delta_1
                delta_1 = delta_1 + 1
            else:
                delta_0 = delta_1
                delta_1 = delta_1

    return abs(cur_x) + abs(cur_y)


def test(cc=None, expected=None, DBG=False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc, DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "*** " + str(cc) + " *** -> Result = " + str(result),
        " -> success = " + str(flag) + " -> expected " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


test(1, 0, True)  #
test(12, 3, True)  #
test(23, 2, True)  #
test(1024, 31, True)  #

INPUT_FILE = "input-d02.txt"

puzzle_input = 347991


result = function(puzzle_input, False)
print(result)

#################
