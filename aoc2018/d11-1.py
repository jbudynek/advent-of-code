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


def build_world(ii, DBG=True):
    x = []
    y = []
    vx = []
    vy = []
    for line in ii:
        if(DBG):print(line)
        nbs = re.findall(r'[-\d]+', line)
        nbs = np.asarray(nbs, dtype=np.int)
        x.append(nbs[0])
        y.append(nbs[1])
        vx.append(nbs[2])
        vy.append(nbs[3])
        
    if(DBG):print(x,y,vx,vy)
    return(x,y,vx,vy)

def display(x,y, values, DBG = True):
    
    s_out = str(values[x,y])+" "+str(values[x+1,y])+" "+str(values[x+2,y])+"\n"
    s_out = s_out +str(values[x,y+1])+" "+str(values[x+1,y+1])+" "+str(values[x+2,y+1])+"\n"
    s_out = s_out +str(values[x,y+2])+" "+str(values[x+1,y+2])+" "+str(values[x+2,y+2])
    total = values[x,y]+values[x+1,y]+values[x+2,y]+values[x,y+1]+values[x+1,y+1]+values[x+2,y+1]+values[x,y+2]+values[x+1,y+2]+values[x+2,y+2]
    print(x,y,total)
    print(s_out)

def function(ii, DBG = True):

    values = {}
    sums = {}

    max_sums = -10000
    x_max_sum = -1
    y_max_sum = -1

    for x in range(1,299):
        for y in range(1,299):
            if (x,y) not in sums:
                sums[(x,y)] = 0
            for dx in range(0,3):
                for dy in range(0,3):
                    if (x+dx,y+dy) not in values:
                        values[(x+dx,y+dy)] = get_power_level(x+dx,y+dy,ii)
                    sums[(x,y)] = sums[(x,y)] + values[(x+dx,y+dy)]
            if sums[(x,y)] > max_sums:
                max_sums = sums[(x,y)]
                x_max_sum = x
                y_max_sum = y

    if (DBG): print(x_max_sum,y_max_sum,max_sums)
    if(DBG):display(x_max_sum,y_max_sum,values)
    #if(DBG):display(33,45,values)

    return (x_max_sum,y_max_sum,max_sums)

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


#print(get_power_level(122,79,57),"-5")
#print(get_power_level(217,196,39),"0")
#print(get_power_level(101,153,71),"4")
#sys.exit()

t1=18
test(t1,(33,45,29),True) 
#sys.exit()

t1=42
test(t1,(21,61,30),True) 
#sys.exit()


#INPUT_FILE="input-d11.txt"
#f = open(INPUT_FILE, "r")
#contents = f.read()
#puzzle_input = contents.splitlines()
#f.close()

ret = function(3031, False) 
print(ret)

# (21, 76, 30)
