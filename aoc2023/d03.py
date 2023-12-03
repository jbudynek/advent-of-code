# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


# parse the input into a complex plane
def parse_engine(all_lines, DBG=True):
    engine = {}
    x = -1
    y = -1
    for line in all_lines:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == ".":
                pass
            elif c in "0123456789":
                engine[complex(x, y)] = int(c)
            else:
                engine[complex(x, y)] = c
    if DBG:
        print(engine)

    return engine


# parse an integer on a line, starting anywhere in the integer,
# not necessarily at the beginning
def parse_int_on_line(z, engine):
    d_z = -1
    cur_z = z
    while cur_z in engine and isinstance(engine[cur_z], int):
        cur_z += d_z
    r = 0
    d_z = 1
    cur_z += d_z
    while cur_z in engine and isinstance(engine[cur_z], int):
        r = r * 10 + engine[cur_z]
        cur_z += d_z
    return r


# On every entry in the plane, when it's a symbol, not a number,
# rotate around to find the integers that are adjacent to the symbol.
# Return a list of tuples: (symbol, list of integers around)
# to be processed in the caller function.
def scan_engine(engine, DBG):
    dirs8 = [complex(1, 1) ** (i) / 2 ** (i // 2) for i in range(8)]
    symbols_and_values = []
    for z, val in engine.items():
        if not isinstance(val, int):
            around = set()
            for d in dirs8:
                if z + d in engine and isinstance(engine[z + d], int):
                    pi = parse_int_on_line(z + d, engine)
                    if DBG:
                        print(engine[z + d], pi)
                    around.add(pi)
            symbols_and_values.append((val, list(around)))
    return symbols_and_values


# Main function
################


def boom_part1(input_val, DBG=True):
    engine = parse_engine(input_val, DBG)
    symbols_and_values = scan_engine(engine, DBG)
    # sum all the integers
    return sum([sum(t[1]) for t in symbols_and_values])


def boom_part2(input_val, DBG=True):
    engine = parse_engine(input_val, DBG)
    symbols_and_values = scan_engine(engine, DBG)
    # sum the products of integers around a "*" only if you have two of those
    return sum(
        [
            (t[1][0] * t[1][1])
            for t in symbols_and_values
            if t[0] == "*" and len(t[1]) == 2
        ]
    )


# Test cases
#############


t1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 4361, True)
test_func(boom_part2, tt1, 467835, True)

# Real data
############

puzzle_input = read_input_file("input-d03.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 507214
# Part 2 solution: 72553319
