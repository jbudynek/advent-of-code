# coding: utf-8

from boilerplate import read_input_file, run_func, test_func


def count_neighbors(field, z):
    dirs = [complex(1, 1) ** (i) / 2 ** (i // 2) for i in range(8)]
    count = sum([field[z + d] for d in dirs if z + d in field])
    return count


def print_f(field, x_min, x_max, y_min, y_max):
    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if complex(xx, yy) in field:
                ss += str(field[complex(xx, yy)])
            else:
                ss += " "
        print(ss)


def parse_field(input_val):
    x_min, x_max, y_min, y_max = 0, len(input_val[0]), 0, len(input_val)

    field = {
        complex(x, y): (1 if input_val[y][x] == "#" else 0)
        for y in range(y_max)
        for x in range(x_max)
    }
    return x_min, x_max, y_min, y_max, field


def conway(input_val, ticks, fixed_corners, DBG):

    x_min, x_max, y_min, y_max, field = parse_field(input_val)

    if fixed_corners:
        field[complex(x_min, y_min)] = 1
        field[complex(x_max - 1, y_min)] = 1
        field[complex(x_max - 1, y_max - 1)] = 1
        field[complex(x_min, y_max - 1)] = 1

    for _ in range(ticks):
        new_field = field.copy()
        for k in field.keys():
            nn = count_neighbors(field, k)
            if field[k] == 1:
                if nn == 2 or nn == 3:
                    new_field[k] = 1
                else:
                    new_field[k] = 0
            else:
                if nn == 3:
                    new_field[k] = 1
                else:
                    new_field[k] = 0
        if fixed_corners:
            new_field[complex(x_min, y_min)] = 1
            new_field[complex(x_max - 1, y_min)] = 1
            new_field[complex(x_max - 1, y_max - 1)] = 1
            new_field[complex(x_min, y_max - 1)] = 1
        # if DBG:print_f(field,  x_min, x_max, y_min, y_max)
        field = new_field
    return sum(field.values())


def boom_part1(input_val, DBG=True):
    return conway(input_val, 100, False, DBG)


def boom_part2(input_val, DBG=True):
    return conway(input_val, 100, True, DBG)


# Test cases
#############


t1 = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 4, True)  # 100 steps -> 4
test_func(boom_part2, tt1, 7, True)  # 100 steps -> 7

# Real data
############

puzzle_input = read_input_file("input-d18.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 814
# PART 2 OK = 924
