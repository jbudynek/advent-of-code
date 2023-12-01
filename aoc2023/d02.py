# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func


def ints_in_string(line):
    ii = list(map(int, re.findall(r"-?\d+", line)))
    return ii


# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
def count_cubes_in_game(line, DBG):
    rounds = re.split(r"[;:]+", line)
    id = ints_in_string(rounds[0])[-1]
    r = 0
    g = 0
    b = 0
    for idx in range(len(rounds) - 1):
        shown = rounds[idx + 1]
        parts = shown.split(",")
        for part in parts:
            nb_cubes = ints_in_string(part)[0]
            if "red" in part:
                r = max(r, nb_cubes)
            elif "green" in part:
                g = max(g, nb_cubes)
            elif "blue" in part:
                b = max(b, nb_cubes)
    if DBG:
        print(line, id, r, g, b)
    return id, r, g, b


def boom_part1(input_val, DBG=True):
    ret = 0
    for line in input_val:
        id, r, g, b = count_cubes_in_game(line, DBG)
        if r <= 12 and g <= 13 and b <= 14:
            ret += id
    return ret


def boom_part2(input_val, DBG=True):
    ret = 0
    for line in input_val:
        _, r, g, b = count_cubes_in_game(line, DBG)
        ret += r * g * b
    return ret


# Test cases
#############


t1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 8, True)
test_func(boom_part2, tt1, 2286, True)

# Real data
############

puzzle_input = read_input_file("input-d02.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 2795
# Part 2 solution: 75561
