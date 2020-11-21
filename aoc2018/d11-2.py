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
from collections import deque
import time

def get_power_level(x,y,serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level = power_level + serial_number
    power_level = power_level * rack_id
    power_level = (power_level // 100) % 10
    power_level = power_level - 5
    return power_level

def function(ii, DBG = True):

    serial_number =ii

    power_levels = np.zeros((301,301),np.int32)

    for x in range(1,301):
        for y in range(1,301):
            power_levels[x,y] = get_power_level(x,y,serial_number)

    sums = np.full((301,301,301),-100,np.int32)

    max_sums = -100
    x_max_sum = -1
    y_max_sum = -1
    size_max_sum = -1

    # a bit slow - in practice the maximum is found quickly as seen in the printouts
    for size in range(3,301):
        if(DBG):print(size)
        if(DBG):print(x_max_sum,y_max_sum,size_max_sum,max_sums)

        # Should use list comprehension here
        for x in range(1,302-size):
            for y in range(1,302-size):
                sums[x,y,size] = np.sum(power_levels[x:x+size-1, y:y+size-1])
                if sums[x,y,size] > max_sums:
                    max_sums = sums[x,y,size]
                    x_max_sum = x
                    y_max_sum = y
                    size_max_sum = size-1

    if (DBG): print(x_max_sum,y_max_sum,size_max_sum,max_sums)
    return (x_max_sum,y_max_sum,size_max_sum,max_sums)

def test(cc=None, expected=None, DBG = False):
    start_millis = int(round(time.time() * 1000))
    result = function(cc,DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    if(expected=="None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))    
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")
    return flag


#t1=18
#test(t1,(90,269,16,113),True) 
#sys.exit()

#t1=42
#test(t1,(232,251,12,119),True) 
#sys.exit()

#INPUT_FILE="input-d11.txt"
#f = open(INPUT_FILE, "r")
#contents = f.read()
#puzzle_input = contents.splitlines()
#f.close()

ret = function(3031, True) 
print(ret)

# (234, 108, 16, 160)
