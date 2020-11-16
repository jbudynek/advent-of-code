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

def display(x,y, DBG = True):
    min_x = np.min(x)
    max_x = np.max(x)
    min_y = np.min(y)
    max_y = np.max(y)

    #if(DBG):print(x)
    #if(DBG):print(y)
    #if(DBG):print("x",min_x,max_x,"y",min_y,max_y)

    ll = len(x)  

    w = {}
    for i in range(ll):
        w[(x[i],y[i])] = 1

    out_s = ""
    for yy in range(min_y,max_y+1):
        for xx in range(min_x,max_x+1):
            if (xx,yy) in w:
                out_s = out_s+"#"
            else:  
                out_s = out_s+"."
        out_s = out_s+"\n"
    print(out_s)

def function(ii, DBG = True):
    x,y,vx,vy = build_world(ii,DBG)

    last_x = np.copy(x)
    last_y = np.copy(y)

    cur_delta_x = 1000000
    cur_delta_y = 1000000
    tick = 0
    while(tick<100000):

        d_x = np.max(x) - np.min(x)
        d_y = np.max(y) - np.min(y)

        if(DBG):print(d_x,d_y)

        if d_x > cur_delta_x and d_y > cur_delta_y:
            print("tick-1=",tick-1)
            display(last_x,last_y)
            break

        cur_delta_x = d_x
        cur_delta_y = d_y

        last_x = np.copy(x)
        last_y = np.copy(y)

        x = np.add(x,vx)
        y = np.add(y,vy)
        tick = tick + 1

    print("out tick=",tick)
    return 1


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

t1="""position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
#tt1 = t1.splitlines()
#test(tt1,"HI",True) # 
#sys.exit()


INPUT_FILE="input-d10.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()
ret = function(puzzle_input, False) #
print(ret)

#EKALLKLB
#tick-1= 10227