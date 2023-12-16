# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# Helpers
##########


def print_field_complex(field, x_min, x_max, y_min, y_max):
    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if complex(xx, yy) in field:
                ss += str(field[complex(xx, yy)])
            else:
                ss += " "
        print(ss)


def parse_field_complex(input):
    x_min, x_max, y_min, y_max = 0, len(input[0]), 0, len(input)
    field = {complex(x, y): (input[y][x]) for y in range(y_max) for x in range(x_max)}
    directions = [complex(0, 1) ** i for i in range(4)]
    return field, x_min, x_max, y_min, y_max, directions


def make_path(start, dir, field, directions, paths_todo, cache):
    [RIGHT, DOWN, LEFT, UP] = directions
    cur_z = start
    cur_dir = dir
    path = []
    while True:
        if cur_z not in field:
            return path, paths_todo, cache
        path.append(cur_z)
        if (cur_z, cur_dir) in cache:
            return path, paths_todo, cache
        else:
            cache.add((cur_z, cur_dir))
        if cur_dir == RIGHT:
            if field[cur_z] == "|":
                start = cur_z
                dir1 = UP
                paths_todo.append((start, dir1))
                cur_dir = DOWN
            elif field[cur_z] == "-":
                pass
            elif field[cur_z] == "/":
                cur_dir = UP
            elif field[cur_z] == "\\":
                cur_dir = DOWN
        elif cur_dir == LEFT:
            if field[cur_z] == "|":
                start = cur_z
                dir1 = UP
                paths_todo.append((start, dir1))
                cur_dir = DOWN
            elif field[cur_z] == "-":
                pass
            elif field[cur_z] == "/":
                cur_dir = DOWN
            elif field[cur_z] == "\\":
                cur_dir = UP
        elif cur_dir == UP:
            if field[cur_z] == "|":
                pass
            elif field[cur_z] == "-":
                start = cur_z
                dir1 = RIGHT
                paths_todo.append((start, dir1))
                cur_dir = LEFT
            elif field[cur_z] == "/":
                cur_dir = RIGHT
            elif field[cur_z] == "\\":
                cur_dir = LEFT
        elif cur_dir == DOWN:
            if field[cur_z] == "|":
                pass
            elif field[cur_z] == "-":
                start = cur_z
                dir1 = RIGHT
                paths_todo.append((start, dir1))
                cur_dir = LEFT
            elif field[cur_z] == "/":
                cur_dir = LEFT
            elif field[cur_z] == "\\":
                cur_dir = RIGHT
        cur_z += cur_dir


def count_energized_cells(field, directions, start0, dir0):
    paths_todo = [(start0, dir0)]
    paths_done = []
    cache = set()

    while len(paths_todo) > 0:
        start = paths_todo[0][0]
        dir = paths_todo[0][1]
        del paths_todo[0]
        path, paths_todo, cache = make_path(
            start, dir, field, directions, paths_todo, cache
        )
        paths_done.append(path)

    count_cells = {}
    for path in paths_done:
        for p in path:
            count_cells[p] = 1

    return len(count_cells.items())


def boom_part1(ipt, DBG=True):
    field, x_min, x_max, y_min, y_max, directions = parse_field_complex(ipt)
    if DBG:
        print_field_complex(field, x_min, x_max, y_min, y_max)
    return count_energized_cells(field, directions, (0 + 0j), (1 + 0j))


#########################


def boom_part2(ipt, DBG=True):
    field, x_min, x_max, y_min, y_max, directions = parse_field_complex(ipt)
    [RIGHT, DOWN, LEFT, UP] = directions

    max_cells = 0

    for x in range(x_min, x_max):
        for y in [y_min, y_max - 1]:
            start0 = complex(x, y)
            dir0 = UP
            if y == y_min:
                dir0 = DOWN
            energy = count_energized_cells(field, directions, start0, dir0)
            max_cells = max(max_cells, energy)

    for x in [x_min, x_max - 1]:
        for y in range(y_min, y_max):
            start0 = complex(x, y)
            dir0 = LEFT
            if x == x_min:
                dir0 = RIGHT
            energy = count_energized_cells(field, directions, start0, dir0)
            max_cells = max(max_cells, energy)

    return max_cells


# Test cases
#############


ipt_test1 = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".splitlines()
test_func(boom_part1, ipt_test1, 46, True)
test_func(boom_part2, ipt_test1, 51, True)

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

# Part 1 solution: 7623
# Part 2 solution: 8244
