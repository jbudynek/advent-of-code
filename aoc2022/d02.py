# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# Main function
##########

scores = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3 + 0,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2 + 0,
    "C Z": 3 + 3,
}

scores2 = {
    "A X": 3 + 0,
    "A Y": 1 + 3,
    "A Z": 2 + 6,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 2 + 0,
    "C Y": 3 + 3,
    "C Z": 1 + 6,
}


def boom_part1(input_val, DBG=True):
    score = 0
    for line in input_val:
        score += scores[line]
    return score


def boom_part2(input_val, DBG=True):
    score = 0
    for line in input_val:
        score += scores2[line]
    return score


# Test cases
##########

tt1 = """A Y
B X
C Z"""
tt1 = tt1.splitlines()  # type: ignore
test_func(boom_part1, tt1, 15, True)
test_func(boom_part2, tt1, 12, True)

# Real data
##########

puzzle_input = read_input_file("input-d02.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 10816
# PART 2 OK = 11657
