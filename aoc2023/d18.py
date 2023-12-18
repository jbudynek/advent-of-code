# coding: utf-8
from boilerplate import read_input_file, run_func, test_func
from shapely.geometry import Polygon


def get_area(path):
    coords = [(int(z.real), int(z.imag)) for z in path]
    poly = Polygon(coords)
    ans = poly.area + poly.length // 2 + 1
    return int(ans)


def boom_part1(ipt, DBG=True):
    cur_z = 0 + 0j
    dirs = {
        "R": 1,
        "L": -1,
        "U": 1j,
        "D": -1j,
    }

    path = [cur_z]

    for line in ipt:
        [dir, dist, color] = line.split()
        dist = int(dist)
        cur_z += dist * dirs[dir]
        path.append(cur_z)

    return get_area(path)


def boom_part2(ipt, DBG=True):
    cur_z = 0 + 0j
    dirs = {
        "0": 1,
        "2": -1,
        "3": 1j,
        "1": -1j,
    }

    path = [cur_z]

    for line in ipt:
        color = line.split()[2]
        dir = color[7]
        dist = int(color[2:7], 16)
        cur_z += dist * dirs[dir]
        path.append(cur_z)

    return get_area(path)


# Test cases
#############


ipt_test1 = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()
test_func(boom_part1, ipt_test1, 62, True)
test_func(boom_part2, ipt_test1, 952408144115, True)

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 40131
# Part 2 solution: 104454050898331
