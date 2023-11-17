# coding: utf-8
import re

from boilerplate import read_input_file, run_func


# Main function
################
def process_input_val(input_val, check_amounts):

    dict_ticker_tape = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    # Example: Sue 5: goldfish: 1, trees: 3, perfumes: 10
    # Rules: cats and trees readings indicates that there are greater than
    # Rules: pomeranians and goldfish readings indicate that there are fewer than

    all_sue_aunties = []
    for line in input_val:
        candidate_aunt_sue = True
        line_split = line.split(" ")
        aunt_sue_id = int(line_split[1][:-1])
        for idx in range((len(line_split) - 1) // 2):
            thing = line_split[(2 * idx) + 2][:-1]
            amount = list(map(int, re.findall(r"-?\d+", line_split[(2 * idx) + 3])))[0]
            if thing not in dict_ticker_tape.keys():
                candidate_aunt_sue = False
                break
            if check_amounts and ("cats" == thing or "trees" == thing):
                if dict_ticker_tape[thing] > amount:
                    candidate_aunt_sue = False
                    break
            elif check_amounts and ("pomeranians" == thing or "goldfish" == thing):
                if dict_ticker_tape[thing] <= amount:
                    candidate_aunt_sue = False
                    break
            elif dict_ticker_tape[thing] != amount:
                candidate_aunt_sue = False
                break
        if candidate_aunt_sue:
            all_sue_aunties.append(aunt_sue_id)

    return all_sue_aunties


def boom_part1(input_val, DBG=True):
    return process_input_val(input_val, False)


def boom_part2(input_val, DBG=True):
    return process_input_val(input_val, True)


# Real data
############

puzzle_input = read_input_file("input-d16.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 103
# PART 2 OK = 405
