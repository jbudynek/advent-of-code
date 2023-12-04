# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func

# Main function
################


def parse_line(line, DBG):
    ss = re.split(r"[:|]+", line)
    id = int(ss[0].split()[1])
    draw = set(map(int, re.findall(r"-?\d+", ss[1])))
    cards = set(map(int, re.findall(r"-?\d+", ss[2])))
    intersect = cards.intersection(draw)
    return id, len(intersect)


def get_score(line, DBG):
    _, nb_match = parse_line(line, DBG)
    if nb_match == 0:
        return 0
    else:
        return 2 ** (nb_match - 1)


def boom_part1(input_val, DBG=True):
    return sum([get_score(line, DBG) for line in input_val])


def boom_part2(input_val, DBG=True):
    all_input_cards = {}
    all_output_cards = []

    for line in input_val:
        id, nb_match = parse_line(line, DBG)
        all_input_cards[id] = nb_match
        all_output_cards.append((id, all_input_cards[id]))

    idx = 0
    while idx < len(all_output_cards):
        (id, nb_match) = all_output_cards[idx]

        for x in range(1, nb_match + 1):
            all_output_cards.append((id + x, all_input_cards[id + x]))
        idx += 1

    return len(all_output_cards)


# Test cases
#############


t1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 13, True)
test_func(boom_part2, tt1, 30, True)

# Real data
############

puzzle_input = read_input_file("input-d04.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 18653
# Part 2 solution: 5921508
