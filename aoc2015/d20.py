# coding: utf-8

import numpy as np
from boilerplate import run_func

# crible d'érathostène


def run(input_val, nb_per_house, max_delivery, DBG=True):
    n = int(input_val)
    n_over_ten = n // nb_per_house

    all_houses = np.zeros(n_over_ten + 1)

    for idx in range(1, n_over_ten + 1):
        k = 0
        for jdx in range(idx, n_over_ten + 1, idx):
            k += 1
            all_houses[jdx] += idx * nb_per_house
            if k == max_delivery:
                break

    mask = np.array(all_houses) < n
    index = np.argmin(mask)
    if DBG:
        print(index)
    return index


def boom_part1(input_val, DBG=True):
    return run(input_val, 10, -1, DBG)


def boom_part2(input_val, DBG=True):
    return run(input_val, 11, 50, DBG)


# Real data
############

puzzle_input = "36000000"

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 831600
# PART 2 OK = 884520
