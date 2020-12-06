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

def end_cur_group(groups_answers, groups_people, cur_group_answers, cur_group_people, nb_yes, DBG = True):
    groups_answers.append(cur_group_answers)
    groups_people.append(cur_group_people)
    
    if DBG: print(cur_group_answers, len(cur_group_answers), cur_group_people)
    for qq in cur_group_answers:
        if cur_group_answers[qq] == cur_group_people:
            nb_yes = nb_yes+1
    return nb_yes


def boom(input_val, DBG = True):
    groups_answers = []
    groups_people = []

    cur_group_answers = {}
    cur_group_people = 0
    nb_yes = 0

    for line in input_val:
        if (line==''):
            nb_yes = end_cur_group(groups_answers, groups_people, cur_group_answers, cur_group_people, nb_yes, DBG)
            cur_group_answers = {}
            cur_group_people = 0
        else:
            cur_group_people = cur_group_people+1
            for q in line:
                if not q in cur_group_answers:
                    cur_group_answers[q] = 0
                cur_group_answers[q] = cur_group_answers[q] + 1

    nb_yes = end_cur_group(groups_answers, groups_people, cur_group_answers, cur_group_people, nb_yes, DBG)

    return nb_yes

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


t1="""abc

a
b
c

ab
ac

a
a
a
a

b"""
tt1 = t1.splitlines()
test(tt1,6,True)
#sys.exit()

INPUT_FILE="input-d06.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False) 
print(ret)

# part 2 = 3197