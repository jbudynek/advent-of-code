import re

import matplotlib.pyplot as plt
import numpy as np

ipt = open("input.txt").read().split("\n")

xmax, ymax = 101, 103
ticks = 100

robots_p = []
robots_v = []
for line in ipt:
    ll = list(map(int, re.findall(r"-?\d+", line)))
    if len(ll) > 0:
        robots_p.append(complex(ll[0], ll[1]))
        robots_v.append(complex(ll[2], ll[3]))

robots_p_0 = robots_p.copy()

r1, r2 = 0, 0
count_quadrants = [0, 0, 0, 0]
for i in range(len(robots_p)):
    robots_p[i] += ticks * robots_v[i]
    robots_p[i] = complex(robots_p[i].real % xmax, robots_p[i].imag % ymax)

    if (robots_p[i].real < xmax // 2) and (robots_p[i].imag < ymax // 2):
        count_quadrants[0] += 1
    elif (robots_p[i].real > xmax // 2) and (robots_p[i].imag < ymax // 2):
        count_quadrants[1] += 1
    elif (robots_p[i].real < xmax // 2) and (robots_p[i].imag > ymax // 2):
        count_quadrants[2] += 1
    elif (robots_p[i].real > xmax // 2) and (robots_p[i].imag > ymax // 2):
        count_quadrants[3] += 1

r1 = count_quadrants[0] * count_quadrants[1] * count_quadrants[2] * count_quadrants[3]

print(f"# Part 1 solution: {r1}")


def longest_sequence_in_matrix(matrix):
    def longest_sequence(arr):
        max_len = 0
        current_len = 0
        for value in arr:
            if value != 0:
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0
        return max_len

    longest = 0
    # Check rows
    for row in matrix:
        longest = max(longest, longest_sequence(row))
    # Check columns
    for col in matrix.T:
        longest = max(longest, longest_sequence(col))
    return longest


robots_p = robots_p_0
longest_seq = 0
tick = 0
while tick <= 8000:
    tick += 1
    for i in range(len(robots_p)):
        robots_p[i] = robots_p[i] + robots_v[i]
        robots_p[i] = complex(robots_p[i].real % xmax, robots_p[i].imag % ymax)

    world = np.zeros((xmax, ymax))
    for i in range(len(robots_p)):
        world[int(robots_p[i].real), int(robots_p[i].imag)] = 1

    l_seq = longest_sequence_in_matrix(world)
    if l_seq > longest_seq:
        longest_seq = l_seq
        print("**", tick, l_seq)
        _, _ = plt.subplots(figsize=(6, 6))
        plt.axis("off")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.imshow(1 - world.T, cmap="RdYlGn")
        plt.savefig(f"out/tree_{tick:04}.png")
        r2 = tick


print(f"# Part 2 solution: {r2}")

# Part 1 solution: 229868730
# Part 2 solution: 7861
