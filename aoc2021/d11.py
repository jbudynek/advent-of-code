# coding: utf-8
from collections import Counter
from timeit import default_timer as timer


# Helpers
##########

def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if(DBG):
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0]-1
    x_max = max(coords, key=lambda t: t[0])[0]+1
    y_min = min(coords, key=lambda t: t[1])[1]-1
    y_max = max(coords, key=lambda t: t[1])[1]+1

    if(DBG):
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max+1):
        ss = ""
        for xx in range(x_min, x_max+1):
            if (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)


def create_world(ccc, DBG=True):
    field = {}
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            field[(x, y)] = int(c)

    if DBG:
        print(field)

    return field


# Main function
##########


def flash(flasher, octopuses, flashers, flashed):
    dirs = [(1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)]

    for d in dirs:
        nxy = (flasher[0]+d[0], flasher[1]+d[1])
        if nxy in octopuses:
            octopuses[nxy] += 1
            if octopuses[nxy] > 9 and nxy not in flashed:
                flashers.add(nxy)

    flashed.add(flasher)
    return


def run_step(octopuses, DBG):
    flashers = set()
    flashed = set()
    for octopus in octopuses.keys():
        octopuses[octopus] += 1
        if octopuses[octopus] > 9:
            flashers.add(octopus)

    while len(flashers) != 0:
        flasher = flashers.pop()
        flash(flasher, octopuses, flashers, flashed)

    for f in flashed:
        octopuses[f] = 0


def boom_part1(input_val, DBG=True):
    octopuses = create_world(input_val, DBG)

    total_flashes = 0

    for step in range(1, 101):

        run_step(octopuses, DBG)
        if DBG:
            print("step", step)
            print_field(octopuses)

        total_flashes += Counter(octopuses.values())[0]

    return total_flashes


def boom_part2(input_val, DBG=True):
    octopuses = create_world(input_val, DBG)
    size = len(octopuses.keys())

    step = 0
    while(True):
        step += 1
        run_step(octopuses, DBG)
        if DBG:
            print("step", step)
            print_field(octopuses)

        nb_flashes = Counter(octopuses.values())[0]
        if nb_flashes == size:
            return step


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
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


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)

# Test cases
##########


tt1 = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
tt1 = tt1.splitlines()
test_part1(tt1, 1656, True)
test_part2(tt1, 195, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d11.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 1743
# PART 2 OK = 364
