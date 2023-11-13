# coding: utf-8
import time

import numpy as np


def get_wire_value(wire, wire_to_formula, wire_to_value, DBG=False):
    if DBG:
        print(wire, wire_to_value)

    if wire in wire_to_value:
        return wire_to_value[wire]
    try:
        formula = wire_to_formula[wire]
    except KeyError:
        return np.uint16(wire)

    try:
        lri = np.uint16(formula)
        wire_to_value[wire] = lri
    except ValueError:
        lll = formula.split(" ")
        if len(lll) == 1:  # assign
            wire_to_value[wire] = get_wire_value(
                lll[0], wire_to_formula, wire_to_value, DBG
            )
        elif len(lll) == 2:  # NOT
            wire_to_value[wire] = ~get_wire_value(
                lll[1], wire_to_formula, wire_to_value, DBG
            )
        elif lll[1] == "AND":
            wire_to_value[wire] = get_wire_value(
                lll[0], wire_to_formula, wire_to_value, DBG
            ) & get_wire_value(lll[2], wire_to_formula, wire_to_value, DBG)
        elif lll[1] == "OR":
            wire_to_value[wire] = get_wire_value(
                lll[0], wire_to_formula, wire_to_value, DBG
            ) | get_wire_value(lll[2], wire_to_formula, wire_to_value, DBG)
        elif lll[1] == "LSHIFT":
            wire_to_value[wire] = get_wire_value(
                lll[0], wire_to_formula, wire_to_value, DBG
            ) << int(lll[2])
        elif lll[1] == "RSHIFT":
            wire_to_value[wire] = get_wire_value(
                lll[0], wire_to_formula, wire_to_value, DBG
            ) >> int(lll[2])

    return wire_to_value[wire]


def boom(input_val, DBG=True):
    wire_to_value = {}
    wire_to_formula = {}

    for ddi in input_val:
        lr = ddi.split(" -> ")
        formula = lr[0]
        wire = lr[1]
        wire_to_formula[wire] = formula

    if DBG:
        print(wire_to_formula)

    for wire, formula in wire_to_formula.items():
        if wire in wire_to_value:
            pass
        else:
            wire_to_value[wire] = get_wire_value(
                wire, wire_to_formula, wire_to_value, DBG
            )

    if "a" in wire_to_value:
        return wire_to_value["a"]
    else:
        return wire_to_value


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


tt1 = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""
test(tt1.splitlines(), -1, True)

INPUT_FILE = "input-d07.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# 3176 OK PART 1
