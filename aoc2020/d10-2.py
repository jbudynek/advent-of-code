# coding: utf-8
import time

import numpy as np


# number of combinations for nb_adapters 1-separated adapters
def get_nb_comb(nb_adapters, DBG=True):
    if nb_adapters == 1:
        return 1
    if nb_adapters == 2:
        return 1
    if nb_adapters == 3:
        return 2
    if nb_adapters == 4:
        return 4
    if nb_adapters == 5:
        return 7
    print("***", nb_adapters)
    return -1


def boom(input_val, DBG=True):

    # find chunks of 1-separated adapters,
    # bounded on the left and right by separation of 3
    # for each chunk compute number of possibilities
    # multiply all that

    numbers = np.asarray(input_val, dtype=np.int)
    numbers = np.sort(numbers)

    numbers = np.append(numbers, max(numbers) + 3)
    numbers = np.insert(numbers, 0, 0)

    if DBG:
        print(numbers)

    ln = len(numbers)
    nb_comb = 1
    left_idx = 0
    right_idx = 1
    while right_idx < ln:
        while numbers[right_idx] - numbers[right_idx - 1] == 1:
            right_idx = right_idx + 1

        if DBG:
            print(numbers[left_idx : right_idx + 1], left_idx, right_idx)  # noqa

        nb_adapters = right_idx - left_idx
        if DBG:
            print(nb_adapters)
        nbc = get_nb_comb(nb_adapters, DBG)
        if DBG:
            print("nbc", nbc)
        nb_comb = nb_comb * nbc

        left_idx = right_idx
        right_idx = left_idx + 1

    if DBG:
        print(numbers[left_idx : right_idx + 1], left_idx, right_idx)  # noqa

    nb_adapters = right_idx - left_idx
    if DBG:
        print(nb_adapters)
    nbc = get_nb_comb(nb_adapters, DBG)
    if DBG:
        print("nbc", nbc)
    nb_comb = nb_comb * nbc

    return nb_comb


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
test(tt1, 8, True)
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
test(tt1, 19208, False)
# sys.exit()

INPUT_FILE = "input-d10.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 2 = 3022415986688
