# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func

# Main function
################


def parse_input(input_val, DBG=True):
    names = []
    capacity = []
    durability = []
    flavor = []
    texture = []
    calories = []

    for line in input_val:
        ss = re.split(r"[ ,;:]+", line)
        names.append(ss[0])
        capacity.append(int(ss[2]))
        durability.append(int(ss[4]))
        flavor.append(int(ss[6]))
        texture.append(int(ss[8]))
        calories.append(int(ss[10]))

    return len(names), capacity, durability, flavor, texture, calories


def generate_all_possible_sums(len_names):
    all_possible_sums = []
    if len_names == 4:
        for a in range(1, 100):
            for b in range(1, 100):
                for c in range(1, 100):
                    d = 100 - a - b - c
                    if d > 0:
                        all_possible_sums.append([a, b, c, d])
    elif len_names == 2:
        for a in range(1, 100):
            b = 100 - a
            if b > 0:
                all_possible_sums.append([a, b])
    else:
        quit("wrong number of entries")
    return all_possible_sums


def get_max_score(
    all_possible_sums,
    len_names,
    capacity,
    durability,
    flavor,
    texture,
    calories,
    count_calories,
):
    max_score = 0
    for sum_split in all_possible_sums:
        total_capacity = 0
        total_durability = 0
        total_flavor = 0
        total_texture = 0
        total_calories = 0
        for idx in range(len_names):
            total_capacity += sum_split[idx] * capacity[idx]
            total_durability += sum_split[idx] * durability[idx]
            total_flavor += sum_split[idx] * flavor[idx]
            total_texture += sum_split[idx] * texture[idx]
            total_calories += sum_split[idx] * calories[idx]
        total_capacity = max(0, total_capacity)
        total_durability = max(0, total_durability)
        total_flavor = max(0, total_flavor)
        total_texture = max(0, total_texture)
        score = total_capacity * total_durability * total_flavor * total_texture
        if (not count_calories) or (count_calories and total_calories == 500):
            max_score = max(max_score, score)
    return max_score


def boom_part1(input_val, DBG=True):
    len_names, capacity, durability, flavor, texture, calories = parse_input(
        input_val, DBG
    )
    all_possible_sums = generate_all_possible_sums(len_names)
    max_score = get_max_score(
        all_possible_sums,
        len_names,
        capacity,
        durability,
        flavor,
        texture,
        calories,
        False,
    )
    return max_score


def boom_part2(input_val, DBG=True):
    len_names, capacity, durability, flavor, texture, calories = parse_input(
        input_val, DBG
    )
    all_possible_sums = generate_all_possible_sums(len_names)
    max_score = get_max_score(
        all_possible_sums,
        len_names,
        capacity,
        durability,
        flavor,
        texture,
        calories,
        True,
    )
    return max_score


# Test cases
#############

t1 = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 62842880, True)
test_func(boom_part2, tt1, 57600000, True)

# Real data
############

puzzle_input = read_input_file("input-d15.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 18965440
# PART 2 OK = 15862900
