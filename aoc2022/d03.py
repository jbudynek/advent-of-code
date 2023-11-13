# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# Main function
##########


def get_common_item(rucksacks):
    common = set(rucksacks[0])
    for r in range(1, len(rucksacks)):
        common = common.intersection(set(rucksacks[r]))
    return list(common)[0]


def get_priority(c):
    if c.islower():
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 27


def boom_part1(input_val, DBG=True):
    priorities = []
    for rucksack in input_val:
        left = rucksack[0 : len(rucksack) // 2]  # noqa
        right = rucksack[len(rucksack) // 2 :]  # noqa
        common = get_common_item([left, right])
        priorities.append(get_priority(common))
    return sum(priorities)


def boom_part2(input_val, DBG=True):
    priorities = []
    for i in range(0, len(input_val), 3):
        badge = get_common_item([input_val[i], input_val[i + 1], input_val[i + 2]])
        priorities.append(get_priority(list(badge)[0]))
    return sum(priorities)


# Test cases
##########


tt1 = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
tt1 = tt1.splitlines()  # type: ignore # type: ignore
test_func(boom_part1, tt1, 157, True)
test_func(boom_part2, tt1, 70, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d03.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 7553
# PART 2 OK = 2758
