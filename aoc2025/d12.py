import re
import numpy as np

# it turns out you can simply compute
# if there is enough room on the grid
# versus the number of '#' characters

ipt_test = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2""".split(
    "\n\n"
)

ipt_puzzle = open("input.txt").read().split("\n\n")

ipt = ipt_puzzle

# ipt = ipt_test

shapes = []
for i in range(len(ipt) - 1):
    lines = ipt[i].splitlines()
    shape = np.zeros((3, 3), dtype=int)
    for y in [0, 1, 2]:
        for x in [0, 1, 2]:
            if lines[y + 1][x] == "#":
                shape[x, y] = 1
    shapes.append(shape)

regions = []
for r in ipt[-1].splitlines():
    integers = list(map(int, re.findall(r"\d+", r)))
    size = (integers[0], integers[1])
    nb_boxes = integers[2:]
    regions.append((size, nb_boxes))


def region_fits(region, shapes):
    (xx, yy) = region[0]
    nb_boxes = region[1]

    nb_hash = 0
    for i, n in enumerate(nb_boxes):
        nb_hash += np.sum(shapes[i]) * n
    if nb_hash >= xx * yy:
        return False

    return True


res1 = sum([region_fits(r, shapes) for r in regions])

print(f"# Part 1 solution: {res1}")

# Part 1 solution: 433
