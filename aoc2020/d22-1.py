# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
import copy
import operator
import re
import string
import sys
import time
from collections import deque
from timeit import default_timer as timer

import numpy as np

# simple implementation of rules using a queue implemented by deque


def parse_cards(input_val, DBG):

    player_to_hand = {}
    hand = deque()
    for ii in input_val:
        if ii.startswith("Player"):
            player = np.asarray(re.findall(r'\d+', ii), dtype=np.int)[0]
            hand = deque()
        elif ii == "":
            player_to_hand[player] = hand
        else:
            hand.append(int(ii))

    player_to_hand[player] = hand

    if DBG:
        print(player_to_hand)

    return player_to_hand


def print_decks(player_to_hand):
    nb_players = len(player_to_hand)
    for p in range(1, nb_players+1):
        print("Player's ", p, "'s deck: ", player_to_hand[p])


def play_round(player_to_hand, DBG):
    nb_players = len(player_to_hand)
    if DBG:
        print_decks(player_to_hand)
    draw = {}
    for p in range(1, nb_players+1):
        draw[p] = player_to_hand[p].popleft()
        if DBG:
            print("Player ", p, " plays: ", draw[p])
    winner = max(draw.items(), key=operator.itemgetter(1))[0]
    if DBG:
        print("Player ", winner, " wins the round!")
    player_to_hand[winner].append(draw[winner])
    done = False
    for p in range(1, nb_players+1):
        if not p == winner:
            player_to_hand[winner].append(draw[p])
        if not player_to_hand[p]:  # empty hand
            done = True
    return(done, winner)


def compute_score(hand):
    ret = 0
    val = 1
    while hand:  # test that hand is not empty
        ret = ret + hand.pop() * val
        val = val + 1
    return ret


def boom(input_val, DBG=True):
    player_to_hand = parse_cards(input_val, DBG)

    round = 1
    winner = None
    while(True):
        if DBG:
            print("-- Round ", round, " --")
        (done, winner) = play_round(player_to_hand, DBG)
        if (done):
            break
        round = round + 1

    if(DBG):
        print("== Post-game results ==")
        print_decks(player_to_hand)

    score = compute_score(player_to_hand[winner])

    return score


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag

########


t1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


tt1 = t1.splitlines()
test(tt1, 306, True)
# sys.exit()

#########

INPUT_FILE = "input-d22.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 1 = 33393
