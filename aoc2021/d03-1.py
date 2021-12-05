# coding: utf-8
import numpy as np


def boom(input_val, DBG=True):

    leng = len(input_val[0])
    gamma = ""
    epsilon = ""

    for k in range(leng):
        nb_0 = 0
        nb_1 = 1
        for ll in input_val:
            if ll[k] == '0':
                nb_0 += 1
            if ll[k] == '1':
                nb_1 += 1
        if nb_0 < nb_1:
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'

    return int(gamma, 2)*int(epsilon, 2)

#############


INPUT_FILE = "input-d03.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)

print(ret)


# PART 1 - 3687446 OK
