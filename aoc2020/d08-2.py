# coding: utf-8
import numpy as np
import re
import copy
import sys
import networkx as nx
#import matplotlib.pyplot as plt
#import operator
#from collections import defaultdict
#from collections import Counter
#from collections import deque
import time

def process(command, idx, acc, DBG = True):
    if DBG:print(command)

    cc = command.split(" ")
    cmd = cc[0]
    val = int(cc[1])
    if DBG:print(cmd,val)

    if (cmd=="nop"):
        idx = idx + 1
        pass
    elif (cmd=="acc"):
        acc = acc + val
        idx = idx + 1
        pass
    elif (cmd=="jmp"):
        idx = idx + val
        pass

    return (idx, acc)
  
def boom(input_val, DBG = True):

    nbinst = len(input_val)
    i = 0

    for i in range(nbinst):
        instructions = input_val.copy()

        if "nop" in instructions[i]: 
            instructions[i] = instructions[i].replace("nop","jmp")
        elif "jmp" in instructions[i]: 
            instructions[i] = instructions[i].replace("jmp","nop")

        if DBG: print(instructions)

        idx = 0
        acc = 0
        idxs = []
        while(True):
            (idx_new, acc_new) = process(instructions[idx], idx, acc, DBG)
            if (idx_new in idxs):
                break
                #return (-1,acc) # loop
            elif (idx_new >= len(instructions)):
                return (0, acc_new) # ok termination
            idx = idx_new
            acc = acc_new
            idxs.append(idx)

    return (-1,-1)

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


t1="""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
tt1 = t1.splitlines()
test(tt1,(0,8),True)
#sys.exit()


INPUT_FILE="input-d08.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False) 
print(ret)

# part 2 = 1543