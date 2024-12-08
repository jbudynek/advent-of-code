# We read the world into a complex plane (dict indexed by x+j*y). We write a
# routine that takes the world as input, and walks the guard step by step.
# We remember each visited point (in a set) to answer part 1 (size of the set).
# We also remember each tuple (visited, direction) to see if we walked the place
# before with the same direction, in which case it's a loop (part 2)
# Part 1 is just one walk, and for part 2 we used "almost brute force" and
# tried to put an obstacle in each spot traveled by the guard in part 1.
# It takes a bit of time but it works :P

ipt = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()

ipt = open("input.txt").read().splitlines()

world = {}
guard_z0 = complex(0, 0)
dzs = [complex(0, 1) ** i for i in range(4)]
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        if c == "^":
            guard_z0 = complex(x, y)
            world[guard_z0] = "."
        else:
            world[complex(x, y)] = c


def walk_patrol(w):
    guard_z = guard_z0
    guard_dz_idx = 3
    visited_with_dir = set()
    visited_with_dir.add((guard_z, guard_dz_idx))
    visited = set()
    visited.add(guard_z)
    while True:
        next_z = guard_z + dzs[guard_dz_idx]
        if next_z not in w:
            break
        else:
            if w[next_z] == "#":
                guard_dz_idx = (guard_dz_idx + 1) % 4
                if (guard_z, guard_dz_idx) in visited_with_dir:
                    return (visited, True)
                visited_with_dir.add((guard_z, guard_dz_idx))
            else:
                guard_z = next_z
                if (guard_z, guard_dz_idx) in visited_with_dir:
                    return (visited, True)
                visited_with_dir.add((guard_z, guard_dz_idx))
                visited.add(next_z)
    return (visited, False)


result1, result2 = 0, 0
path, _ = walk_patrol(world)
result1 = len(path)

print(f"# Part 1 solution: {result1}")

for key in path:
    if world[key] == ".":
        world2 = world.copy()
        world2[key] = "#"
        if walk_patrol(world2)[1]:
            result2 += 1

print(f"# Part 2 solution: {result2}")

# Part 1 solution: 4973
# Part 2 solution: 1482
