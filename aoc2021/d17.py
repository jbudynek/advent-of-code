# coding: utf-8
import re
from timeit import default_timer as timer

import numpy as np

# Main function
##########


def parse_bounds(str):
    rr = np.asarray(re.findall(r"-?\d+", str), dtype=int)
    return (rr[0], rr[1], rr[2], rr[3])


def make_step(position, velocity):
    position += velocity
    if velocity.real > 0:
        velocity = velocity + complex(-1, -1)
    elif velocity.real < 0:
        velocity = velocity + complex(1, -1)
    else:
        velocity = velocity + complex(0, -1)

    return (position, velocity)


def in_target(position, xmin, xmax, ymin, ymax):
    return (
        xmin <= position.real
        and position.real <= xmax
        and ymin <= position.imag
        and position.imag <= ymax
    )


def below_target(position, xmin, xmax, ymin, ymax):
    return position.imag < ymin


def launch(velocity, xmin, xmax, ymin, ymax):
    position = complex(0, 0)
    step = 0
    y_max = 0
    while True:
        step += 1
        (position, velocity) = make_step(position, velocity)
        y_max = max(y_max, int(position.imag))
        if in_target(position, xmin, xmax, ymin, ymax):
            return (y_max, True)
        if below_target(position, xmin, xmax, ymin, ymax):
            return (y_max, False)


def boom_part1(input_val, DBG=True):
    (xmin, xmax, ymin, ymax) = parse_bounds(input_val[0])
    top_y = -1
    max_x = max(xmin, xmax)
    max_y = abs(min(ymin, ymax))
    for vx in range(1, max_x):
        for vy in range(1, max_y):
            velocity = complex(vx, vy)
            (y, _) = launch(velocity, xmin, xmax, ymin, ymax)
            top_y = max(y, top_y)
    return top_y


def boom_part2(input_val, DBG=True):
    (xmin, xmax, ymin, ymax) = parse_bounds(input_val[0])
    ret = 0
    max_x = max(xmin, xmax)
    max_y = abs(min(ymin, ymax))
    for vx in range(2 * max_x):
        for vy in range(-2 * max_y, 2 * max_y):
            velocity = complex(vx, vy)
            (_, inside) = launch(velocity, xmin, xmax, ymin, ymax)
            if inside:
                ret += 1
    return ret


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


tt1 = "target area: x=20..30, y=-10..-5"
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 45, True)
test_part2(tt1, 112, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d17.txt"
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

# PART 1 OK = 4005
# PART 2 OK = 2953
