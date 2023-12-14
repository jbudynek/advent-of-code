# coding: utf-8

from boilerplate import read_input_file, run_func, test_func


def print_field(field, x_max, y_max):
    for yy in range(y_max + 1):
        ss = ""
        for xx in range(x_max + 1):
            if (xx, yy) in field:
                ss += str(field[(xx, yy)])
            else:
                ss += " "
        print(ss)


def parse_world(input):

    x_max, y_max = len(input[0]), len(input)

    field = {(x, y): (input[y][x]) for y in range(y_max) for x in range(x_max)}

    return field, x_max, y_max


# Main function
################


def get_load(field, x_max, y_max):
    ans = 0
    for y in range(y_max):
        for x in range(x_max):
            ans += (field[x, y] == "O") * (y_max - y)
    return ans


def boom_part1(ipt, DBG=True):
    field, x_max, y_max = parse_world(ipt)
    for y in range(y_max):
        for yy in range(y, 0, -1):
            for x in range(x_max):
                if (
                    (x, yy) in field
                    and field[(x, yy)] == "O"
                    and (x, yy - 1) in field
                    and field[(x, yy - 1)] == "."
                ):
                    field[(x, yy)], field[(x, yy - 1)] = (".", "O")
        if DBG:
            print_field(field, x_max, y_max)
    return get_load(field, x_max, y_max)


def boom_part2(ipt, DBG=True):
    field, x_max, y_max = parse_world(ipt)

    field2field_cycle = {}
    cycle2load = {}

    for cycle in range(1_000_000_000):
        if DBG and cycle % 100000 == 0:
            print(cycle)
        if str(field) in field2field_cycle:
            f1, c1 = field2field_cycle[str(field)]
            field = f1
            len_cycle = cycle - c1
            d = (1_000_000000 - c1) % len_cycle
            return cycle2load[d + c1 - 1]
        else:
            f0 = field.copy()
            # north
            for y in range(y_max):
                for yy in range(y, 0, -1):
                    for x in range(x_max):
                        if (
                            (x, yy) in field
                            and field[(x, yy)] == "O"
                            and (x, yy - 1) in field
                            and field[(x, yy - 1)] == "."
                        ):
                            field[(x, yy)], field[(x, yy - 1)] = (".", "O")
            if DBG:
                print_field(field, x_max, y_max)
            # west
            for x in range(x_max):
                for xx in range(x, 0, -1):
                    for y in range(y_max):
                        if (
                            (xx, y) in field
                            and field[(xx, y)] == "O"
                            and (xx - 1, y) in field
                            and field[(xx - 1, y)] == "."
                        ):
                            field[(xx, y)], field[(xx - 1, y)] = (".", "O")
            if DBG:
                print_field(field, x_max, y_max)
            # south
            for y in range(y_max, 0, -1):
                for yy in range(y):
                    for x in range(x_max):
                        if (
                            (x, yy) in field
                            and field[(x, yy)] == "O"
                            and (x, yy + 1) in field
                            and field[(x, yy + 1)] == "."
                        ):
                            field[(x, yy)], field[(x, yy + 1)] = (".", "O")
            if DBG:
                print_field(field, x_max, y_max)
            # east
            for x in range(x_max, 0, -1):
                for xx in range(x):
                    for y in range(y_max):
                        if (
                            (xx, y) in field
                            and field[(xx, y)] == "O"
                            and (xx + 1, y) in field
                            and field[(xx + 1, y)] == "."
                        ):
                            field[(xx, y)], field[(xx + 1, y)] = (".", "O")
            if DBG:
                print_field(field, x_max, y_max)
            if DBG:
                print(cycle, get_load(field, x_max, y_max))
            cycle2load[cycle] = get_load(field, x_max, y_max)
            field2field_cycle[str(f0)] = (field, cycle)

    return get_load(field, x_max, y_max)


# Test cases
#############


ipt_test1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()
test_func(boom_part1, ipt_test1, 136, True)
test_func(boom_part2, ipt_test1, 64, False)
# quit()

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 111979
# Part 2 solution: 102055
