# coding: utf-8
from boilerplate import *
import itertools

# Main function
##########


def build_world(input_val):
    a_2_b = {}
    people = []

    for line in input_val:
        ll = line.split()
        if ll[2] == "lose":
            a_2_b[ll[0] + "_" + ll[10][:-1]] = -int(ll[3])
        else:
            a_2_b[ll[0] + "_" + ll[10][:-1]] = int(ll[3])
        if ll[0] not in people:
            people.append(ll[0])

    return a_2_b, people


def get_max_happ(a_2_b, people):
    max_happ = 0
    for p in itertools.permutations(people):
        happ = 0
        table = list(p)
        for i in range(len(people)):
            happ += a_2_b[table[i] + "_" + table[(i + 1) % len(table)]]
            happ += a_2_b[table[(i + 1) % len(table)] + "_" + table[i]]
        max_happ = max(max_happ, happ)
    return max_happ


def boom_part1(input_val, DBG=True):
    a_2_b, people = build_world(input_val)
    max_happ = get_max_happ(a_2_b, people)
    return max_happ


def boom_part2(input_val, DBG=True):
    a_2_b, people = build_world(input_val)

    # add me
    jb = "JULIEN"
    for p in people:
        a_2_b[jb + "_" + p] = 0
        a_2_b[p + "_" + jb] = 0

    people.append(jb)

    max_happ = get_max_happ(a_2_b, people)
    return max_happ


# Test cases
##########

tt1 = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""
tt1 = tt1.splitlines()
test_func(boom_part1, tt1, 330, True)

# Real data
##########

puzzle_input = read_input_file("input-d13.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 733
# PART 2 OK = 725
