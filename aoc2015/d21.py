# coding: utf-8
from itertools import combinations

from boilerplate import read_input_file, run_func

# stolen and adapted from the solution megathread
# https://www.reddit.com/r/adventofcode/comments/3xnyoi/day_21_solutions/
# https://www.reddit.com/r/adventofcode/comments/3xnyoi/comment/cy6kife/


def parse_rules():
    shop = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3""".splitlines()
    weapons = [line.split() for line in shop[1:6]]
    armors = [line.split() for line in shop[8:13]]
    rings = [line.split() for line in shop[15:]]
    armors.append([0 for i in range(4)])
    rings.extend([[0 for i in range(5)] for j in range(2)])
    return weapons, armors, rings


def parse_boss(input_val):
    boss_hp = int(input_val[0].split()[-1])
    boss_damage = int(input_val[1].split()[-1])
    boss_armor = int(input_val[2].split()[-1])
    return boss_hp, boss_damage, boss_armor


def damage_to_boss(my_weapon, my_ring_1_2, boss_armor):
    return max(
        1,
        int(my_weapon[2])
        + int(my_ring_1_2[0][3])
        + int(my_ring_1_2[1][3])
        - boss_armor,
    )


def damage_to_me(my_armor, my_ring_1_2, boss_damage):
    return max(
        1,
        boss_damage
        - int(my_armor[3])
        - int(my_ring_1_2[0][4])
        - int(my_ring_1_2[1][4]),
    )


def run(input_val, win_lose, min_max):
    weapons, armors, rings = parse_rules()
    boss_hp, boss_damage, boss_armor = parse_boss(input_val)
    my_hp = 100
    ret = min_max(
        [
            int(my_weapon[1])
            + int(my_armor[1])
            + int(my_ring_1_2[0][2])
            + int(my_ring_1_2[1][2])
            for my_weapon in weapons
            for my_armor in armors
            for my_ring_1_2 in combinations(rings, 2)
            if win_lose(
                ((boss_hp - 1) // damage_to_boss(my_weapon, my_ring_1_2, boss_armor)),
                ((my_hp - 1) // damage_to_me(my_armor, my_ring_1_2, boss_damage)),
            )
        ]
    )
    return ret


def lte(lhs, rhs):
    return lhs <= rhs


def gt(lhs, rhs):
    return lhs > rhs


def boom_part1(input_val, DBG=True):
    ret = run(input_val, lte, min)
    return ret


def boom_part2(input_val, DBG=True):
    ret = run(input_val, gt, max)
    return ret


# Real data
############

puzzle_input = read_input_file("input-d21.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 91
# PART 2 OK = 158
