# coding: utf-8
import re
import time
from collections import deque

import numpy as np


def display(id_player, placed_marbles, next_marble):
    ss = ""
    ss = ss + "[" + str(id_player) + "] "
    for i in range(len(placed_marbles)):
        ss = ss + "" + str(placed_marbles[i]) + " "
    ss = ss + " - next=" + str(next_marble)
    print(ss)


def function(ii, DBG=True):
    start_millis = int(round(time.time() * 1000))

    nbs = re.findall(r"\d+", ii)
    nbs = np.asarray(nbs, dtype=np.int)
    nb_players = nbs[0]
    nb_marbles = nbs[1] * 100
    if DBG:
        print(nb_players, nb_marbles)
    scores = {}
    placed_marbles = deque()
    placed_marbles.appendleft(0)
    next_marble = 1
    id_player = 0
    while next_marble <= nb_marbles:
        if next_marble % (nb_marbles // 20) == 0:
            cur_millis = int(round(time.time() * 1000))
            print(
                next_marble,
                "/",
                nb_marbles,
                "**",
                int(next_marble / nb_marbles * 100),
                "%",
                (cur_millis - start_millis),
                "ms",
                int((cur_millis - start_millis) / 1000),
                "s",
                int((cur_millis - start_millis) / 1000 / 60),
                "min",
            )
        if next_marble % 23 == 0:
            # deal with multiples of 23
            # if(DBG):print("23", next_marble)
            placed_marbles.rotate(-7)
            bonus = placed_marbles.popleft()
            placed_marbles.rotate(1)
            if id_player not in scores:
                scores[id_player] = 0
            scores[id_player] = scores[id_player] + next_marble + bonus
            if DBG:
                print(
                    "["
                    + str(id_player)
                    + "]"
                    + " score = "
                    + str(scores[id_player])
                    + " dscore = "
                    + str(next_marble + bonus)
                    + " next_marble = "
                    + str(next_marble)
                    + " bonus = "
                    + str(bonus)
                )
        else:
            placed_marbles.rotate(1)
            placed_marbles.appendleft(next_marble)
        next_marble = next_marble + 1
        id_player = (id_player + 1) % nb_players
        if DBG:
            display(id_player, placed_marbles, next_marble)
        # if(next_marble==50):sys.exit()
    if DBG:
        print(placed_marbles)
    if DBG:
        print(scores)
    return max(scores.values())


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


# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305
# t1="9 players; last marble is worth 25 points"
# tt1 = t1.splitlines()
# test(t1,32,True) #
# sys.exit()
# t1="10 players; last marble is worth 1618 points"
# test(t1,8317,False) #
# sys.exit()
# t1="13 players; last marble is worth 7999 points"
# test(t1,146373,False) #
# sys.exit()
# t1="30 players; last marble is worth 5807 points"
# test(t1,37305,False) #
# sys.exit()
# INPUT_FILE="input-d09.txt"
# f = open(INPUT_FILE, "r")
# contents = f.read()
# puzzle_input = contents.splitlines()
puzzle_input = "405 players; last marble is worth 71700 points"
# f.close()
ret = test(puzzle_input)  #
print(ret)
