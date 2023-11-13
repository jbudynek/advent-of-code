# coding: utf-8
import time


def parse_instruction(instruction, DBG=True):
    action = instruction[0]
    value = int(instruction[1:])
    return (action, value)


def process_instruction(z, direction, action, value, DBG):
    new_direction = direction
    new_z = z
    # turn the ship
    if action == "R":
        quarter = value // 90
        new_direction = direction * ((-1j) ** quarter)
    elif action == "L":
        quarter = value // 90
        new_direction = direction * ((1j) ** quarter)
    # move the ship forward
    elif action == "F":
        new_z = z + direction * value
    # move the ship in cardinal directions
    elif action == "N":
        new_z = z + 1j * value
    elif action == "S":
        new_z = z - 1j * value
    elif action == "W":
        new_z = z - 1 * value
    elif action == "E":
        new_z = z + 1 * value
    return (new_z, new_direction)


def boom(input_val, DBG=True):

    cur_z = complex(0, 0)
    cur_direction = complex(1, 0)

    for instruction in input_val:
        if DBG:
            print(cur_z, cur_direction)
        (action, value) = parse_instruction(instruction, DBG)
        if DBG:
            print(action, value)
        (new_z, new_direction) = process_instruction(
            cur_z, cur_direction, action, value, DBG
        )
        if DBG:
            print(new_z, new_direction)
        cur_z = new_z
        cur_direction = new_direction

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
test(tt1, 25, True)
# sys.exit()

INPUT_FILE = "input-d12.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=True)
print(ret)

# part 1 = 420
