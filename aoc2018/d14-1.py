# coding: utf-8
import time

import numpy as np


def boom(input_val, DBG=True):

    nb_recipes = input_val

    nb_elves = 2

    indexes = np.arange(nb_elves)

    scores = np.full(nb_recipes + 11, "A")
    scores[0] = "3"
    scores[1] = "7"
    nb_scores = 2

    while nb_scores < nb_recipes + 10:
        # combine recipes = sum scores of all indexes and append each number at
        # the end of scores
        ingredients = scores[indexes].astype(int)
        new_recipe = np.sum(ingredients)
        for num in str(new_recipe):
            scores[nb_scores] = num
            nb_scores = nb_scores + 1
        for ii in range(len(indexes)):
            indexes[ii] = (1 + indexes[ii] + int(scores[indexes[ii]])) % nb_scores
        if DBG:
            print("".join(scores), indexes)

    ret = ""
    for ii in range(10):
        ret = ret + scores[ii + nb_recipes]

    return ret


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


# tt1=9
# test(tt1,"5158916779",True)
# #sys.exit()

# tt1=5
# test(tt1,"0124515891",True)
# #sys.exit()

# tt1=18
# test(tt1,"9251071085",True)
# #sys.exit()

# tt1=2018
# test(tt1,"5941429882",True)
# sys.exit()

# INPUT_FILE="input-d14.txt"
# f = open(INPUT_FILE, "r")
# contents = f.read()
# puzzle_input = contents.splitlines()
# f.close()

puzzle_input = 380621
ret = boom(puzzle_input, False)
print(ret)

# 6985103122
