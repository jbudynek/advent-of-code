# coding: utf-8

import numpy as np
import re
import copy
import sys
import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
from collections import Counter
import time


def display(id_player, placed_marbles, cur_marble_index, next_marble):
    ss = ""
    ss = ss + "["+str(id_player) + "] "
    for i in range(len(placed_marbles)):
        if (i==cur_marble_index):
            ss = ss + "*"+str(placed_marbles[i])+"* "
        else:
            ss = ss + ""+str(placed_marbles[i])+" "
    ss = ss + " - next="+str(next_marble)
    print(ss)

def function(ii, DBG = True):

    nbs = re.findall(r'\d+', ii)
    nbs = np.asarray(nbs, dtype=np.int)
    nb_players = nbs[0]
    nb_marbles = nbs[1]
    if(DBG):print(nb_players,nb_marbles)
    

    scores = {}



    placed_marbles = np.arange(1)
    next_marble = 1
    cur_marble_index = 0
    id_player = 0
    while(next_marble<=nb_marbles):
        if (next_marble % 23 == 0):
            # deal with multiples of 23
            #if(DBG):print("23", next_marble)
            cur_marble_index = (cur_marble_index - 7)%len(placed_marbles)
            bonus = placed_marbles[cur_marble_index]
            placed_marbles = np.delete(placed_marbles,cur_marble_index)
            if not id_player in scores:
                scores[id_player] = 0
            scores[id_player] = scores[id_player] + next_marble + bonus
            if(DBG):print("["+str(id_player)+"]" + " score = "+ str(scores[id_player])+ " dscore = "+ str(next_marble+bonus))
        else:
            next_position = (cur_marble_index + 1) #% len(placed_marbles)
            next_next_position = ((cur_marble_index + 2) % len(placed_marbles))
            if next_next_position==0:
                next_next_position = len(placed_marbles)
            placed_marbles = np.insert(placed_marbles,next_next_position,next_marble)
            #if(DBG):print(cur_marble_index, placed_marbles)
            cur_marble_index = next_next_position

        next_marble = next_marble + 1
        id_player = ( id_player + 1 ) % nb_players
        #if(DBG):display(id_player, placed_marbles, cur_marble_index, next_marble)


    if(DBG):print(placed_marbles)
    if(DBG):print(scores)


    return max(scores.values())


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))

    result = str(function(cc,DBG))

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")



# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305

#t1="9 players; last marble is worth 25 points"
#tt1 = t1.splitlines()
#test(t1,32,True) # 
#sys.exit()

t1="10 players; last marble is worth 1618 points"
test(t1,8317,True) # 

t1="13 players; last marble is worth 7999 points"
test(t1,146373,True) # 


INPUT_FILE="input-d09.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
#puzzle_input = contents.splitlines()
puzzle_input = contents.rstrip()
f.close()

ret = function(puzzle_input,False) # 
print(ret)
