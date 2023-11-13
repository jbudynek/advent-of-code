# coding: utf-8
import time


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
            else:
                field[(x, y)] = c

    if DBG:
        print(field)
    return field


def boom(input_val, DBG=True):
    world = create_world(input_val, DBG)

    x_max = len(input_val[0])
    y_max = len(input_val)

    count_trees = 0
    cur_x = 0
    cur_y = 0
    dx = 3
    dy = 1
    while cur_y < y_max:
        if (cur_x, cur_y) in world:
            count_trees = count_trees + 1
        cur_x = (cur_x + dx) % x_max
        cur_y = cur_y + dy
    return count_trees


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


t1 = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
tt1 = t1.splitlines()
test(tt1, 7, True)
# sys.exit()

INPUT_FILE = "input-d03.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 1 = 198
