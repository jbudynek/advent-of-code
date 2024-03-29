# coding: utf-8
import sys
import time

CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"

RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"

RED_BG = "\x1b[101m"
GREEN_BG = "\x1b[102m"
YELLOW_BG = "\x1b[103m"
DEFAULT_BG = "\x1b[49m"


def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)


#        sys.stdout.write(CURSOR_UP_ONE)
#        sys.stdout.write(ERASE_LINE)


def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0] - 1
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1] - 1
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)

    # delete_last_lines(y_max-y_min)


def print_tracks_and_vehicles(xyids, vehicles, vehicles_id_to_v_and_count, DBG=True):
    coords = xyids.keys()
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0] - 1
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1] - 1
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                if (xx, yy) in vehicles:
                    v = vehicles_id_to_v_and_count[vehicles[(xx, yy)]][0]
                    ss += RED_BG + str(v) + DEFAULT_BG
                else:
                    ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)

    # delete_last_lines(y_max-y_min)


def create_world(ccc, DBG=True):
    field = {}
    vehicles = {}
    vehicles_id_to_v_and_count = {}
    x = -1
    y = -1
    v_id = 0
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == " " or c == "#":
                continue
            elif c == "<" or c == ">":
                field[(x, y)] = "-"
                vehicles[(x, y)] = v_id
                vehicles_id_to_v_and_count[v_id] = (c, 0)
                v_id = v_id + 1
            elif c == "^" or c == "v":
                field[(x, y)] = "|"
                vehicles[(x, y)] = v_id
                vehicles_id_to_v_and_count[v_id] = (c, 0)
                v_id = v_id + 1
            else:
                field[(x, y)] = c

    if DBG:
        print(field)
    if DBG:
        print_tracks_and_vehicles(field, vehicles, vehicles_id_to_v_and_count)

    return (field, vehicles, vehicles_id_to_v_and_count)


def move_vehicle(x, y, v, count, tracks, DBG=True):
    if v == "^":
        y = y - 1
        if tracks[(x, y)] == "/":
            v = ">"
        elif tracks[(x, y)] == "\\":
            v = "<"
        elif tracks[(x, y)] == "+":
            if count == 0:  # left
                v = "<"
            elif count == 1:  # straight
                pass
            elif count == 2:  # right
                v = ">"
            count = (count + 1) % 3
    elif v == "v":
        y = y + 1
        if tracks[(x, y)] == "/":
            v = "<"
        elif tracks[(x, y)] == "\\":
            v = ">"
        elif tracks[(x, y)] == "+":
            if count == 0:  # left
                v = ">"
            elif count == 1:  # straight
                pass
            elif count == 2:  # right
                v = "<"
            count = (count + 1) % 3
    elif v == ">":
        x = x + 1
        if tracks[(x, y)] == "/":
            v = "^"
        elif tracks[(x, y)] == "\\":
            v = "v"
        elif tracks[(x, y)] == "+":
            if count == 0:  # left
                v = "^"
            elif count == 1:  # straight
                pass
            elif count == 2:  # right
                v = "v"
            count = (count + 1) % 3
    elif v == "<":
        x = x - 1
        if tracks[(x, y)] == "/":
            v = "v"
        elif tracks[(x, y)] == "\\":
            v = "^"
        elif tracks[(x, y)] == "+":
            if count == 0:  # left
                v = "v"
            elif count == 1:  # straight
                pass
            elif count == 2:  # right
                v = "^"
            count = (count + 1) % 3
    return (x, y, v, count)


def function(ii, DBG=True):

    # parse tracks and vehicles from input
    (tracks, vehicles, vehicles_id_to_v_and_count) = create_world(ii, DBG)

    print("***")
    print(vehicles)
    print(len(vehicles))
    print_tracks_and_vehicles(tracks, vehicles, vehicles_id_to_v_and_count, False)

    tick = 0
    # start tick
    # sort vehicles along y then x, iterate on them
    # if vehicle still there, move it
    # check for collision
    # remove both vehicles if collision
    # end tick
    # until only one vehicle

    while len(vehicles) > 1:
        # aa=input()
        tick = tick + 1

        for key in sorted(vehicles, key=lambda xy: (xy[1] * 1000 + xy[0])):
            x = key[0]
            y = key[1]
            if (x, y) in vehicles:
                v_id = vehicles[(x, y)]
                if DBG:
                    print(v_id)
                v = vehicles_id_to_v_and_count[v_id][0]
                count = vehicles_id_to_v_and_count[v_id][1]
                (new_x, new_y, new_v, new_count) = move_vehicle(
                    x, y, v, count, tracks, DBG
                )
                if (new_x, new_y) in vehicles:  # collision
                    v_id_2 = vehicles[(new_x, new_y)]
                    del vehicles[(x, y)]
                    del vehicles[(new_x, new_y)]
                    del vehicles_id_to_v_and_count[v_id]
                    del vehicles_id_to_v_and_count[v_id_2]
                else:  # update position
                    del vehicles[(x, y)]
                    vehicles[(new_x, new_y)] = v_id
                    vehicles_id_to_v_and_count[v_id] = (new_v, new_count)
        if DBG:
            print(tick)
        if DBG:
            print(vehicles)
        if DBG:
            print(len(vehicles))
        if DBG:
            print_tracks_and_vehicles(tracks, vehicles, vehicles_id_to_v_and_count)
        if len(vehicles) % 2 == 0:
            print(tick)
            print(vehicles)
            print(len(vehicles))
            print("Two vehicles == BUG")
            sys.exit()
        if (tick % 100) == 0:
            print(tick)
            print(vehicles)
            print(len(vehicles))
            # print_tracks_and_vehicles(tracks,vehicles,vehicles_id_to_v_and_count,False)

    # OK we're done
    print(tick)
    print(vehicles)
    print(len(vehicles))
    print_tracks_and_vehicles(tracks, vehicles, vehicles_id_to_v_and_count, False)
    (x, y) = next(iter(vehicles))
    return (x, y, tick)


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = function(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
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
    return flag


t1 = r"""
 v
 |
 \---\
     |
     \---\
         |
         ^
 v
 \---\
     |
     \---\
         |
         ^

     /-
     |
     |
     v
   /-/
   ^
   |
   |
 >-/

   /-<
   |
   |
   |
 /-/
 |
 |
 |
-/

"""
tt1 = t1.splitlines()
# test(tt1,(6,4,3),True)
# sys.exit()

INPUT_FILE = "input-d13.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input, False)
print(ret)

# (145,88, 10748)
