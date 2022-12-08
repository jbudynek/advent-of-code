# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


def create_world_complex(input):

    x_min, x_max, y_min, y_max = 0, len(input[0]), 0, len(input)

    field = {
        complex(x, y): int(input[y][x]) for y in range(y_max) for x in range(x_max)
    }

    directions = [complex(0, 1) ** i for i in range(4)]

    return field, x_min, x_max, y_min, y_max, directions


def get_scenic_score(field, x, y, directions):
    z_0 = complex(x, y)
    scenic_score = 1
    for dz in directions:
        viewing_distance = 0
        current_z = z_0
        while True:
            current_z = current_z + dz
            if current_z not in field:
                break
            viewing_distance += 1
            if field[current_z] >= field[z_0]:
                break
        scenic_score *= viewing_distance
    return scenic_score


def is_visible(field, x, y, directions):
    z_0 = complex(x, y)
    for dz in directions:
        current_z = z_0
        visible = True
        while True:
            current_z = current_z + dz
            if current_z not in field:
                if visible:
                    return True
                break
            if field[current_z] >= field[z_0]:
                visible = False
                break
    return False


def boom_part1(input_val, DBG=True):
    field, x_min, x_max, y_min, y_max, directions = create_world_complex(input_val)
    return sum(
        [
            is_visible(field, x, y, directions)
            for x in range(x_min, x_max)
            for y in range(y_min, y_max)
        ]
    )


def boom_part2(input_val, DBG=True):
    field, x_min, x_max, y_min, y_max, directions = create_world_complex(input_val)
    return max(
        [
            get_scenic_score(field, x, y, directions)
            for x in range(x_min, x_max)
            for y in range(y_min, y_max)
        ]
    )


# Test cases
##########


t1 = """30373
25512
65332
33549
35390"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 21, True)
test_func(boom_part2, tt1, 8, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d08.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 1816
# PART 2 OK = 383520
