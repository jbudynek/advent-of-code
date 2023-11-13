# coding: utf-8
import time

import numpy as np


def speak_next_number(turn, latest_spoken_number, last_seen, DBG=True):
    if DBG:
        print(turn, latest_spoken_number, last_seen)
    if latest_spoken_number not in last_seen:
        if DBG:
            print("never seen number ", latest_spoken_number)
        last_seen[latest_spoken_number] = (-1, turn)
        return (0, turn + 1, last_seen)
    else:
        if DBG:
            print("already seen number ", latest_spoken_number)
        ls = last_seen[latest_spoken_number]
        if ls[0] == -1:
            if DBG:
                print("number ", latest_spoken_number, " seen only once ", ls)
            if 0 not in last_seen:
                last_seen[0] = (-1, -1)
            ls0 = last_seen[0]
            last_seen[0] = (ls0[1], turn)
            return (0, turn + 1, last_seen)
        else:
            if DBG:
                print("number ", latest_spoken_number, " seen twice ", ls)
            delta = ls[1] - ls[0]
            if delta not in last_seen:
                last_seen[delta] = (-1, -1)
            lsd = last_seen[delta]
            last_seen[delta] = (lsd[1], turn)
            return (delta, turn + 1, last_seen)


def boom(input_val, DBG=True):

    ii = input_val[0].split(",")
    ii = np.asarray(ii, dtype=np.int)

    last_seen = {}
    number = 0
    turn = 0

    for n in ii:
        last_seen[n] = (-1, turn)
        turn = turn + 1
        number = n

    if DBG:
        print(last_seen, turn, "th number spoken is ", number)

    while turn < 30000000:
        new_number, new_turn, last_seen = speak_next_number(
            turn, number, last_seen, DBG=False
        )
        number, turn = new_number, new_turn
        if DBG:
            print(turn, "th number spoken is ", number)

    return number


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


t1 = """0,3,6"""
tt1 = t1.splitlines()
test(tt1, 175594, False)
# sys.exit()

t1 = """1,3,2"""
tt1 = t1.splitlines()
test(tt1, 2578, False)
# sys.exit()

t1 = """2,1,3"""
tt1 = t1.splitlines()
test(tt1, 3544142, False)
# sys.exit()

t1 = """1,2,3"""
tt1 = t1.splitlines()
test(tt1, 261214, False)
# sys.exit()

t1 = """2,3,1"""
tt1 = t1.splitlines()
test(tt1, 6895259, False)
# sys.exit()

t1 = """3,2,1"""
tt1 = t1.splitlines()
test(tt1, 18, False)
# sys.exit()

t1 = """3,1,2"""
tt1 = t1.splitlines()
test(tt1, 362, False)
# sys.exit()


# INPUT_FILE = "input-d14.txt"
# f = open(INPUT_FILE, "r")
# contents = f.read()
# puzzle_input = contents.splitlines()
# f.close()

# each example runs in ~30 sec on my computer

ret = boom("0,14,6,20,1,4".splitlines(), DBG=False)
print(ret)

# part 2 = 8546398
