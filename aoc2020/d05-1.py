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

# also works but too literal 
def boom_0(input_val, DBG = True):
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



t1="FBFBBFFRLR"
test(t1,(44,5,357),True)
#sys.exit()

t1="BFFFBBFRRR"
test(t1,(70,7,567),True)
#sys.exit()

t1="FFFBBBFRRR"
test(t1,(14,7,119),True)
#sys.exit()

t1="BBFFBBFRLL"
test(t1,(102,4,820),True)
#sys.exit()


INPUT_FILE="input-d05.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

max_seat_id = 0
for seat in puzzle_input:
    (row,col,seat_id) = boom(seat, False)
    if seat_id>max_seat_id: max_seat_id= seat_id
print(max_seat_id)

# part 1 = 801