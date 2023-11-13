# coding: utf-8
import time

import numpy as np

# from itertools import combinations


def boom(input_val, DBG=True):

    numbers = np.asarray(input_val, dtype=np.int)
    numbers = np.sort(numbers)
    if DBG:
        print(numbers)

    nb_1 = 1  # charging outlet
    nb_3 = 1  # device adapter

    for idx in range(1, len(numbers)):
        if numbers[idx] - numbers[idx - 1] == 1:
            if DBG:
                print(numbers[idx - 1 : idx + 1], 1)  # noqa
            nb_1 = nb_1 + 1
        elif numbers[idx] - numbers[idx - 1] == 3:
            if DBG:
                print(numbers[idx - 1 : idx + 1], 3)  # noqa
            nb_3 = nb_3 + 1
        else:
            if DBG:
                print(numbers[idx - 1 : idx])  # noqa
            print("***")

    return (nb_1, nb_3, nb_1 * nb_3)


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


t1 = """16
10
15
5
1
11
7
19
6
12
4"""
tt1 = t1.splitlines()
test(tt1, (7, 5, 35), True)
# sys.exit()


t1 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
tt1 = t1.splitlines()
test(tt1, (22, 10, 220), True)
# sys.exit()

INPUT_FILE = "input-d10.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 1 = (66, 32, 2112)
