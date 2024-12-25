ipt_1_3 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""".split(
    "\n\n"
)

ipt = ipt_1_3

ipt = open("input-d25.txt").read().strip().split("\n\n")

locks = []
keys = []

for kl in ipt:
    lines = kl.split("\n")
    www = {complex(x, y): lines[y][x] for y in range(7) for x in range(5)}
    if www[0 + 0j] == "#" and www[4 + 0j] == "#":
        locks.append(www)
    else:
        keys.append(www)


def fit(lock, key):
    for z in lock.keys():
        if lock[z] == "#" and key[z] == "#":
            return False
    return True


r1 = sum([fit(lock, key) for lock in locks for key in keys])

print(f"# Part 1 solution: {r1}")

# Part 1 solution: 2840
