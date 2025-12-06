ipt_test = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test

world = {}
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        world[complex(x, y)] = c

dzs = [complex(1, 1) ** i / 2 ** (i // 2) for i in range(8)]

result1 = 0
for z0 in world.keys():
    if world[z0] != "@":
        continue
    count = 0
    for dz in dzs:
        if world.get(z0 + dz, "") == "@":
            count += 1
    if count < 4:
        result1 += 1

# Part 2 - I'm actually surprised that it worked!

result2 = 0
while True:
    dres = 0
    for z0 in world.keys():
        if world[z0] != "@":
            continue
        count = 0
        for dz in dzs:
            if world.get(z0 + dz, "") == "@":
                count += 1
        if count < 4:
            world[z0] = "."
            dres += 1
    result2 += dres
    if dres == 0:
        break
out1 = []
out2 = []

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 1451
# Part 2 solution: 8701
