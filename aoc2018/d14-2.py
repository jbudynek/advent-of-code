# coding: utf-8
import time

import numpy as np


def boom(input_val, DBG=True):

    # brute force it - quite ugly
    fff = 22000000

    pattern = input_val

    nb_elves = 2

    indexes = np.arange(nb_elves)

    scores = np.full(fff + nb_elves, "A")
    scores[0] = "3"
    scores[1] = "7"
    nb_scores = 2

    while nb_scores < fff:
        # combine recipes = sum scores of all indexes a
        # nd append each number at the end of scores
        ingredients = scores[indexes].astype(int)
        new_recipe = np.sum(ingredients)
        for num in str(new_recipe):
            scores[nb_scores] = num
            nb_scores = nb_scores + 1
            if nb_scores % 1000000 == 0:
                print(nb_scores)
        for ii in range(len(indexes)):
            indexes[ii] = (1 + indexes[ii] + int(scores[indexes[ii]])) % nb_scores
        if DBG:
            print("".join(scores), indexes)

    where = "".join(scores).find(pattern)
    return where


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


# tt1="51589"
# test(tt1,9,False)
# sys.exit()

# tt1="01245"
# test(tt1,5,True)
# #sys.exit()

# tt1="92510"
# test(tt1,18,True)
# #sys.exit()

# tt1="59414"
# test(tt1,2018,True)
# sys.exit()

# INPUT_FILE="input-d14.txt"
# f = open(INPUT_FILE, "r")
# contents = f.read()
# puzzle_input = contents.splitlines()
# f.close()

puzzle_input = "380621"
ret = boom(puzzle_input, False)
print(ret)

# 20182290
