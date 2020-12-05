# coding: utf-8
import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time


def boom(input_val, DBG = True):
    seat = input_val
    min_row=0
    max_row=127

    for k in range(0,7):
        delta = pow(2,6-k)
        if seat[k]=='F':
            min_row = min_row
            max_row = max_row - delta
        else:
            min_row = min_row + delta
            max_row = max_row
        if DBG: print(k,seat[k],min_row,max_row)

    min_col = 0
    max_col = 7

    for k in range(0,3):
        delta = pow(2,2-k)
        if seat[7+k]=='L':
            min_col = min_col
            max_col = max_col - delta
        else:
            min_col = min_col + delta
            max_col = max_col
        if DBG: print(k,seat[7+k],min_col,max_col)

    seat_id = max_row*8+max_col
    if DBG: print(seat,min_col,max_row,seat_id)

    return (max_row,max_col,seat_id)

def test(cc=None, expected=None, DBG = False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc,DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected=="None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))    
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result)+ " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")
    return flag


INPUT_FILE="input-d05.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

seat_ids = []
for seat in puzzle_input:
    (row,col,seat_id) = boom(seat, False)
    seat_ids.append(seat_id)

# sort seat_ids and look for the missing spot
seat_ids = np.sort(seat_ids)
for ii in range(1,len(seat_ids)):
    if (seat_ids[ii]-seat_ids[ii-1]==2):
        print(seat_ids[ii]-1)

# part 2 = 597