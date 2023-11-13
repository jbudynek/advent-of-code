# coding: utf-8

import time

import numpy as np


def build_world(ii, DBG=True):
    world = {}
    xmin = ymin = 1000
    xmax = ymax = 0
    idx = ord("A")
    for line in ii:
        xy = line.split(",")
        xy = np.asarray(xy, dtype=np.int)
        if DBG:
            print(xy, chr(idx))
        world[chr(idx)] = (xy[0], xy[1])
        xmin = min(xmin, xy[0])
        ymin = min(ymin, xy[1])
        xmax = max(xmax, xy[0])
        ymax = max(ymax, xy[1])
        idx = idx + 1
    bbox = (xmin, xmax, ymin, ymax)
    if DBG:
        print(bbox)
    if DBG:
        print(world)
    return (world, bbox)


def manhattan_distance(x0, y0, x1, y1):
    return abs(x1 - x0) + abs(y1 - y0)


def count_area(world, bbox, DBG=True):
    xmin = bbox[0]
    xmax = bbox[1]
    ymin = bbox[2]
    ymax = bbox[3]
    areas = {}
    for key in world:
        areas[key] = 0
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            closest = ""
            closest_dist = 1000
            for key in world:
                target = world[key]
                dist = manhattan_distance(x, y, target[0], target[1])
                if dist < closest_dist:
                    closest_dist = dist
                    closest = key
                elif dist == closest_dist:
                    closest = "."
            if not closest == ".":
                areas[closest] = areas[closest] + 1
    if DBG:
        print(areas)
    return areas


def function(ii, DBG=True):

    # build world = put targets A B C D where they belong
    # find bounding box
    # loop on xy within bouding box
    # in each spot record closest target with Manhattan distance
    # measure areas
    # augment bounding box by 1
    # fill additional spots with closest target
    # measure areas, those that augmented are infinite
    # return biggest in those that did not augment
    # phew

    (world, bbox) = build_world(ii)

    areas1 = count_area(world, bbox)

    bbox2 = (bbox[0] - 1, bbox[1] + 1, bbox[2] - 1, bbox[3] + 1)

    areas2 = count_area(world, bbox2)

    max_area = 0
    for k in areas1:
        if areas1[k] == areas2[k]:
            max_area = max(max_area, areas2[k])

    if DBG:
        print(max_area)
    return max_area


def test(cc=None, expected=None, DBG=False):

    start_millis = int(round(time.time() * 1000))

    result = str(function(cc, DBG))

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "*** " + str(cc) + " *** -> Result = " + str(result),
        " -> success = " + str(flag) + " -> expected " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


t1 = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
tt1 = t1.splitlines()
test(tt1, 17, True)  #

# sys.exit()

INPUT_FILE = "input-d06.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = function(puzzle_input, True)  #
print(ret)
