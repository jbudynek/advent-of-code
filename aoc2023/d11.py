# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


def parse_galaxies(ipt):
    galaxy2coords = {}
    x = -1
    y = -1
    galaxy_id = 0
    for line in ipt:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == "#":
                galaxy2coords[galaxy_id] = (x, y)
                galaxy_id += 1

    return galaxy2coords


def expand(ipt, factor):
    galaxy2coords = parse_galaxies(ipt)

    all_x = [z[0] for z in galaxy2coords.values()]
    all_y = [z[1] for z in galaxy2coords.values()]

    all_empty_x = set(range(min(all_x), max(all_x))).difference(set(all_x))
    all_empty_y = set(range(min(all_y), max(all_y))).difference(set(all_y))

    ans = 0

    all_gal = list(galaxy2coords.keys())
    lg = len(all_gal)
    for i in range(lg):
        for j in range(i + 1, lg):
            l, r = min(galaxy2coords[i][0], galaxy2coords[j][0]), max(
                galaxy2coords[i][0], galaxy2coords[j][0]
            )
            dx = range(l, r)
            d, u = min(galaxy2coords[i][1], galaxy2coords[j][1]), max(
                galaxy2coords[i][1], galaxy2coords[j][1]
            )
            dy = range(d, u)
            nbx = len(dx) + len(all_empty_x.intersection(set(dx))) * (factor - 1)
            nby = len(dy) + len(all_empty_y.intersection(set(dy))) * (factor - 1)
            ans += nbx + nby

    return ans


def boom_part1(ipt, DBG=True):
    return expand(ipt, 2)


def boom_part2(ipt, DBG=True):
    return expand(ipt, 1000000)


# Test cases
#############


ipt_test1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()
test_func(boom_part1, ipt_test1, 374, True)

# returns 82000210 for factor 1000000
test_func(boom_part2, ipt_test1, 82000210, True)

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

# Part 1 solution: 9795148
# Part 2 solution: 650672493820
