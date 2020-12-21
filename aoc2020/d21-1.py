# coding: utf-8
# import networkx as nx
# import matplotlib.pyplot as plt
# import operator
# from collections import defaultdict
# from collections import Counter
# from collections import deque
# from functools import reduce
# from math import log
# from itertools import combinations, permutations, product
import copy
import operator
import re
import string
import sys
import time
from timeit import default_timer as timer

import numpy as np

# this gives the answer for part 1 and part 2

# list all allergens
# one by one, match them like this:
# for each food that has this allergen
# take list of ingredients, remove those that are already matched
# intersect with next list of ingredients
# if intersection has size one, ok it's matched
# otherwise try to match the next unmatched allergen

def parse_food(input_val, DBG):
    food_id_to_ingredients = []
    food_id_to_allergens = []
    allergen_to_food_ids = {}
    fid = 0
    for ii in input_val:
        ss = ii.split("(")
        ingredients = ss[0].rstrip().split(" ")
        food_id_to_ingredients.append(ingredients)
        allergens = ss[1][9:len(ss[1])-1].replace(" ", "").split(",")
        food_id_to_allergens.append(allergens)
        for a in allergens:
            if not a in allergen_to_food_ids:
                allergen_to_food_ids[a] = []
            allergen_to_food_ids[a].append(fid)
        fid = fid + 1
        if DBG:
            print(ii, ingredients, allergens)
    return (food_id_to_ingredients, food_id_to_allergens, allergen_to_food_ids)


def boom(input_val, DBG=True):
    (food_id_to_ingredients, food_id_to_allergens,
     allergen_to_food_ids) = parse_food(input_val, DBG)

    nb_food = len(food_id_to_ingredients)

    all_allergens = set()

    for i in range(nb_food):
        all_allergens.update(food_id_to_allergens[i])

    if DBG:
        print(all_allergens)

    all_allergens = list(all_allergens)

    allergens_left_to_match = all_allergens.copy()

    ingredient_to_allergen = {}

    while(len(allergens_left_to_match) > 0):
        if DBG:
            print(len(allergens_left_to_match), allergens_left_to_match)
        for a in allergens_left_to_match:
            food_ids = allergen_to_food_ids[a]
            candidates_ingredients = {}
            candidates = set()
            for fid in food_ids:
                candidates_ingredients[fid] = set()
                ingredients = food_id_to_ingredients[fid]
                for i in ingredients:
                    if not i in ingredient_to_allergen:
                        candidates_ingredients[fid].add(i)
                if len(candidates) == 0:
                    candidates.update(candidates_ingredients[fid])
                else:
                    candidates = candidates.intersection(
                        candidates_ingredients[fid])
            if len(candidates) == 1:
                ingredient_to_allergen[candidates.pop()] = a
                allergens_left_to_match.remove(a)
            else:
                pass

    if DBG:
        print("***", ingredient_to_allergen)

    inert_count = 0

    for i in range(nb_food):
        ings = food_id_to_ingredients[i]
        for ing in ings:
            if not ing in ingredient_to_allergen:
                inert_count = inert_count + 1
    if DBG:
        print("***inert_count:", inert_count)

    ita_s = {k: v for k, v in sorted(
        ingredient_to_allergen.items(), key=lambda item: item[1])}

    cdil = ''
    for kk in ita_s.keys():
        cdil = cdil + ","+kk

    cdil = cdil[1:]
    if DBG:
        print("***canonical dangerous ingredient:", cdil)

    return (inert_count, cdil)


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag

########


t1 = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


tt1 = t1.splitlines()
test(tt1, (5, "mxmxvkd,sqjhc,fvjkl"), True)
# sys.exit()

#########

INPUT_FILE = "input-d21.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 1 = 2078
# part 2 = lmcqt,kcddk,npxrdnd,cfb,ldkt,fqpt,jtfmtpd,tsch
