# coding: utf-8
from collections import Counter
from timeit import default_timer as timer

# Helpers
##########


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            field[(x, y)] = int(c)

    if DBG:
        print(field)

    return field


# Main function
##########


def get_lows(world):
    total_risk = 0
    lows = []
    # iterate on cells
    for xy in world:
        center_value = world[xy]
        up = world.get((xy[0], xy[1] + 1), 10)
        down = world.get((xy[0], xy[1] - 1), 10)
        left = world.get((xy[0] + 1, xy[1]), 10)
        right = world.get((xy[0] - 1, xy[1]), 10)
        # if all adjacent < center_value
        if (
            (center_value < up)
            and (center_value < down)
            and (center_value < left)
            and (center_value < right)
        ):
            # this is a low point
            # compute risk and save position
            risk = center_value + 1
            total_risk += risk
            lows.append(xy)
    return (lows, total_risk)


def boom_part1(input_val, DBG=True):
    world = create_world(input_val, DBG)
    (_, total_risk) = get_lows(world)
    return total_risk


def explore(tagged_world, where, label, DBG):
    if tagged_world[where] < 0 or tagged_world[where] == 9:
        return tagged_world
    tagged_world[where] = label
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dir in dirs:
        nxy = (where[0] + dir[0], where[1] + dir[1])
        if nxy in tagged_world and tagged_world[nxy] != 9:
            tagged_world = explore(tagged_world, nxy, label, DBG)
    return tagged_world


def boom_part2(input_val, DBG=True):
    world = create_world(input_val, DBG)
    tagged_world = world.copy()
    (lows, _) = get_lows(world)

    label = 0
    for low in lows:
        # explore basin
        label -= 1
        tagged_world = explore(tagged_world, low, label, DBG)

    # 3 biggest
    counter = Counter(tagged_world.values())
    del counter[9]
    counter = counter.most_common(3)
    return counter[0][1] * counter[1][1] * counter[2][1]


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


# Test cases
##########


tt1 = """2199943210
3987894921
9856789892
8767896789
9899965678"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 15, True)
test_part2(tt1, 1134, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d09.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 524
# PART 2 OK = 1235430
