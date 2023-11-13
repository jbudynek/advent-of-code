# coding: utf-8
import time


def parse_instruction(instruction, DBG=True):
    action = instruction[0]
    value = int(instruction[1:])
    return (action, value)


def process_instruction(z, waypoint, action, value, DBG):
    new_z = z
    new_waypoint = waypoint
    # rotate the waypoint
    if action == "R":
        quarter = value // 90
        new_waypoint = waypoint * ((-1j) ** quarter)
    elif action == "L":
        quarter = value // 90
        new_waypoint = waypoint * ((1j) ** quarter)
    # move ship forward along the waypoint
    elif action == "F":
        new_z = z + waypoint * value
    # update waypoint along cardinal directions
    elif action == "N":
        new_waypoint = waypoint + 1j * value
    elif action == "S":
        new_waypoint = waypoint - 1j * value
    elif action == "W":
        new_waypoint = waypoint - 1 * value
    elif action == "E":
        new_waypoint = waypoint + 1 * value
    return (new_z, new_waypoint)


def boom(input_val, DBG=True):

    cur_z = complex(0, 0)
    cur_waypoint = 10 + 1j

    for instruction in input_val:
        if DBG:
            print(cur_z, cur_waypoint)
        (action, value) = parse_instruction(instruction, DBG)
        if DBG:
            print(action, value)
        (new_z, new_waypoint) = process_instruction(
            cur_z, cur_waypoint, action, value, DBG
        )
        if DBG:
            print(new_z, new_waypoint)

        # aa = input()
        cur_z = new_z
        cur_waypoint = new_waypoint

    manhattan = int(abs(cur_z.real) + abs(cur_z.imag))
    return manhattan


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


t1 = """F10
N3
F7
R90
F11"""
tt1 = t1.splitlines()
test(tt1, 286, True)
# sys.exit()

INPUT_FILE = "input-d12.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 42073
