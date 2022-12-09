# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

directions = {
    "U": complex(0, 1),
    "D": complex(0, -1),
    "L": complex(-1, 0),
    "R": complex(1, 0),
}


def parse_line(line):
    ll = line.split()
    n = int(ll[1])
    dz = directions[ll[0]]
    return dz, n


def sign(x):
    # I can't believe this does not exist in Python
    if x == 0:
        return 0
    else:
        return x / abs(x)


def move_tail(head_pos, tail_pos):
    delta = head_pos - tail_pos

    # if the points are adjacent or in the same place, do nothing
    if abs(delta) < 2:
        return tail_pos

    # otherwise move tail towards head by increment of 0 or 1 along x and y
    # they will thus become adjacent
    dx = sign(delta.real)
    dy = sign(delta.imag)
    tail_pos += complex(dx, dy)

    return tail_pos


def boom_part1(input_val, DBG=True):

    cur_head_position = complex(0, 0)
    cur_tail_position = complex(0, 0)
    all_tail_positions = set()

    for line in input_val:
        dz, n = parse_line(line)
        for _ in range(n):
            cur_head_position += dz
            cur_tail_position = move_tail(cur_head_position, cur_tail_position)
            all_tail_positions.add(cur_tail_position)

    return len(all_tail_positions)


def boom_part2(input_val, DBG=True):
    # note: we could rewrite part 1 to use this code by setting rope_length to 1
    cur_head_position = complex(0, 0)
    rope_length = 9
    cur_tails_position = [complex(0, 0) for _ in range(rope_length)]
    all_tail_positions = set()

    for line in input_val:
        dz, n = parse_line(line)
        for _ in range(n):
            cur_head_position += dz
            cur_tails_position[0] = move_tail(cur_head_position, cur_tails_position[0])
            for i in range(1, rope_length):
                cur_tails_position[i] = move_tail(
                    cur_tails_position[i - 1], cur_tails_position[i]
                )
            all_tail_positions.add(cur_tails_position[-1])

    return len(all_tail_positions)


# Test cases
##########


t1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 13, True)

t1 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 36, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d09.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 6209
# PART 2 OK = 2460
