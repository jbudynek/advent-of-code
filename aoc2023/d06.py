# coding: utf-8
import numpy as np
from boilerplate import read_input_file, run_func, test_func


def count_wins(times, distances):
    ret = np.prod(
        [
            sum(
                [
                    (times[idx] - speed) * speed > distances[idx]
                    for speed in range(1, times[idx] + 1)
                ]
            )
            for idx in range(len(times))
        ]
    )
    return ret


def boom_part1(ipt, DBG=True):
    times = [int(t) for t in ipt[0].split()[1:]]
    distances = [int(t) for t in ipt[1].split()[1:]]
    return count_wins(times, distances)


def boom_part2(ipt, DBG=True):
    times = [int("".join(ipt[0].split()[1:]))]
    distances = [int("".join(ipt[1].split()[1:]))]
    return count_wins(times, distances)


# Test cases
#############


t1 = """Time:      7  15   30
Distance:  9  40  200"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 288, True)
test_func(boom_part2, tt1, 71503, True)

# Real data
############

puzzle_input = read_input_file("input-d06.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 4403592
# Part 2 solution: 38017587
