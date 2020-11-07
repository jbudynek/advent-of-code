# coding: utf-8

import numpy as np
import re
import copy
import sys
#import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
from collections import Counter
import time


def function(ii, DBG = True):

    words = ii.split()
    #x = np.array(numbers)
    c = Counter(words)
    most = c.most_common(1)
    if(DBG):print(most)
    count = most[0][1]
    return count==1


def test(cc=None, expected=None, DBG = False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc,DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = (result == expected)
    print("*** "+str(cc) + " *** -> Result = "+str(result), " -> success = "+ str(flag) + " -> expected " + expected)    
    print((stop_millis-start_millis),"ms",int((stop_millis-start_millis)/1000),"s",int((stop_millis-start_millis)/1000/60),"min")


t1="aa bb cc dd ee"
test(t1,True,True) # 

t2 = "aa bb cc dd aa" 
test(t2,False,True) # 

t3 = "aa bb cc dd aaa"
test(t3,False,True) # 

INPUT_FILE="input-d04.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
for pp in puzzle_input:
    result = function(pp,False)
    nn = nn + result
    kk = kk+1
    #if (kk==10):break
print(nn)

#################

