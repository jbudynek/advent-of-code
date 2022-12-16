# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func
from shapely.geometry import LineString, Polygon


def boom_part1(input_val, DBG=True):

    polygon_union = None

    minx = 0
    maxx = 0

    for line in input_val:
        ii = list(map(int, re.findall(r"-?\d+", line)))

        (s_x, s_y) = (ii[0], ii[1])
        (b_x, b_y) = (ii[2], ii[3])

        nyc_dist = abs(s_x - b_x) + abs(s_y - b_y)

        minx = min(minx, s_x - nyc_dist)
        maxx = max(maxx, s_x + nyc_dist)

        p = Polygon(
            [
                (s_x - nyc_dist, s_y),
                (s_x, s_y + nyc_dist),
                (s_x + nyc_dist, s_y),
                (s_x, s_y - nyc_dist),
            ]
        )

        if polygon_union is None:
            polygon_union = p
        else:
            polygon_union = polygon_union.union(p)

    l_1 = LineString([(minx, 10), (maxx, 10)])  # test
    l_2 = LineString([(minx, 2000000), (maxx, 2000000)])  # real

    iii_1 = polygon_union.intersection(l_1)
    iii_2 = polygon_union.intersection(l_2)

    if DBG:
        print(iii_1, iii_2)

    return int(iii_1.length), int(iii_2.length)


def boom_part2(input_val, DBG=True):

    polygon_union = None

    for line in input_val:
        ii = list(map(int, re.findall(r"-?\d+", line)))

        (s_x, s_y) = (ii[0], ii[1])
        (b_x, b_y) = (ii[2], ii[3])

        nyc_dist = abs(s_x - b_x) + abs(s_y - b_y)

        p = Polygon(
            [
                (s_x - nyc_dist, s_y),
                (s_x, s_y + nyc_dist),
                (s_x + nyc_dist, s_y),
                (s_x, s_y - nyc_dist),
            ]
        )

        if polygon_union is None:
            polygon_union = p
        else:
            polygon_union = polygon_union.union(p)

    if DBG:
        print(polygon_union)

    # test data
    square_to_search_into_1 = Polygon([(0, 0), (20, 0), (20, 20), (0, 20)])  # test
    answer_inside_1 = polygon_union.intersection(square_to_search_into_1)

    min_ar_1 = answer_inside_1.area
    small_pol_1 = None
    xx_1 = 0
    yy_1 = 0
    if len(answer_inside_1.interiors) > 0:
        for pol in answer_inside_1.interiors:
            p = Polygon(pol)
            if p.area < min_ar_1:
                min_ar_1 = p.area
                small_pol_1 = p

        (minx_1, miny_1, maxx_1, maxy_1) = small_pol_1.bounds
        xx_1 = int(minx_1 + maxx_1) // 2
        yy_1 = int(miny_1 + maxy_1) // 2

    # real data
    square_to_search_into_2 = Polygon(
        [(0, 0), (4000000, 0), (4000000, 4000000), (0, 4000000)]
    )  # real
    answer_inside_2 = polygon_union.intersection(square_to_search_into_2)

    min_ar_2 = answer_inside_2.area
    small_pol_2 = None
    for pol in answer_inside_2.interiors:
        p = Polygon(pol)
        if p.area < min_ar_2:
            min_ar_2 = p.area
            small_pol_2 = p

    (minx_2, miny_2, maxx_2, maxy_2) = small_pol_2.bounds
    xx_2 = int(minx_2 + maxx_2) // 2
    yy_2 = int(miny_2 + maxy_2) // 2

    return xx_1 * 4000000 + yy_1, xx_2 * 4000000 + yy_2


# Test cases
##########


t1 = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, (26, 0), True)  # y=10
test_func(boom_part2, tt1, (56000011, 56000011), True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d15.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 4873353
# PART 2 OK = 11600823139120
