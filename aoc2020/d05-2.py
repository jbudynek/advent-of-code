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

# turn seat code into binary numbers
def boom(input_val, DBG = True):
    seat = input_val

    row_bin = int(seat[0:7].replace('F','0').replace('B','1'),2)
    col_bin = int(seat[7:10].replace('R','1').replace('L','0'),2)
   
    seat_id = row_bin*8+col_bin
    if DBG: print(seat,row_bin,col_bin,seat_id)

    return (row_bin,col_bin,seat_id)

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