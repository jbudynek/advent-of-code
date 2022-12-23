# coding: utf-8
import sys
from collections import defaultdict

from boilerplate import read_input_file, run_func, test_func


def get_bounds(xyids, DBG):
    coords = xyids
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0]
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1]
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    return (x_min, x_max, y_min, y_max)


def print_field(xyids, DBG):

    (x_min, x_max, y_min, y_max) = get_bounds(xyids, DBG)

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                ss += "#"
            else:
                ss += " "
        print(ss)


def create_world(ccc, DBG):
    field = set()
    x = -1
    y = -1
    for line in ccc:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == "#":
                field.add((x, y))

    if DBG:
        print(field)

    return field


def next_round(field, round):

    # First half
    field_new = set()

    moveable = []
    around_8 = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    ]

    # deal with elves that don't move
    # memorize which ones will consider moving
    for elf in field:
        field_new.add(elf)
        for dir in around_8:
            new_key = (elf[0] + dir[0], elf[1] + dir[1])
            if new_key in field:
                field_new.remove(elf)
                moveable.append(elf)
                break

    #####

    consider = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    to_test = {
        (0, 1): [(-1, 1), (0, 1), (1, 1)],
        (0, -1): [(-1, -1), (0, -1), (1, -1)],
        (-1, 0): [(-1, -1), (-1, 0), (-1, 1)],
        (1, 0): [(1, -1), (1, 0), (1, 1)],
    }

    # if to_test all free
    # try moving to consider
    # put coordinates in a list

    candidates = defaultdict(list)
    for elf in moveable:
        is_candidate = False
        for i in range(round, round + 4):
            dir = consider[i % 4]
            new_key = (elf[0] + dir[0], elf[1] + dir[1])
            to_test_list = to_test[dir]
            idx_ttl = 0
            is_free = True
            while idx_ttl < 3:
                is_it_free = to_test_list[idx_ttl]
                tk = (elf[0] + is_it_free[0], elf[1] + is_it_free[1])
                if tk in field:
                    is_free = False
                idx_ttl += 1
            if is_free:
                candidates[new_key].append(elf)
                is_candidate = True
                break
        if not is_candidate:
            field_new.add(elf)

    # count candidates in each case
    # if one -> move
    # if more -> none of the candidates move

    for key, candidates_list in candidates.items():
        if len(candidates_list) == 1:
            field_new.add(key)
        else:
            for e in candidates_list:
                field_new.add(e)

    return field_new


def boom_part1(input_val, DBG=True):
    elves = create_world(input_val, DBG)
    if DBG:
        print_field(elves, DBG)

    nb_rounds = 10
    for rr in range(nb_rounds):
        elves = next_round(elves, rr)
        if DBG:
            print("round", rr)
        if DBG:
            print_field(elves, DBG)

    (x_min, x_max, y_min, y_max) = get_bounds(elves, DBG)

    area = (x_max - x_min) * (y_max - y_min)
    nb_elves = len(elves)

    return area - nb_elves


def boom_part2(input_val, DBG=True):
    elves = create_world(input_val, DBG)
    if DBG:
        print_field(elves, DBG)

    rr = 0
    while True:
        elves_new = next_round(elves, rr)
        if DBG:
            print("round", rr)
        if DBG:
            print_field(elves_new, DBG)
        if elves == elves_new:
            if DBG:
                print("***", rr)
            return rr + 1
        elves = elves_new
        rr += 1


# Test cases
##########


t1 = """.....
..##.
..#..
.....
..##.
....."""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 25, True)
# sys.exit()

t1 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 110, True)
# sys.exit()
test_func(boom_part2, tt1, 20, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d23.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

sys.exit()

# PART 1 OK = 4049
# PART 2 OK = 1021
