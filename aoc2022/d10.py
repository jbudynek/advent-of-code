# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


def draw(x, current_crt_line, current_crt_index):
    if abs(x - current_crt_index) <= 1:
        current_crt_line += "#"
    else:
        current_crt_line += " "

    current_crt_index += 1
    if current_crt_index % 40 == 0:
        print(current_crt_line)
        current_crt_line = ""
        current_crt_index = 0

    return (current_crt_line, current_crt_index)


def increment_cycle(current_crt_line, current_crt_index, sum_strength, cycle, x):
    cycle += 1
    current_crt_line, current_crt_index = draw(x, current_crt_line, current_crt_index)
    if (cycle - 20) % 40 == 0:
        sum_strength += x * cycle
    return cycle, sum_strength, current_crt_line, current_crt_index


def boom_part1(input_val, DBG=True):
    current_crt_line = ""
    current_crt_index = 0

    # 20 60 100 140 180 220

    sum_strength = 0
    instruction_idx = 0
    cycle = 0
    x = 1
    while cycle < 241:
        if instruction_idx >= len(input_val):
            break
        line = input_val[instruction_idx]
        instruction_idx += 1
        if line.startswith("addx"):
            dx = int(line.split()[1])
            cycle, sum_strength, current_crt_line, current_crt_index = increment_cycle(
                current_crt_line, current_crt_index, sum_strength, cycle, x
            )
            cycle, sum_strength, current_crt_line, current_crt_index = increment_cycle(
                current_crt_line, current_crt_index, sum_strength, cycle, x
            )
            x = x + dx
        elif line.startswith("noop"):
            cycle, sum_strength, current_crt_line, current_crt_index = increment_cycle(
                current_crt_line, current_crt_index, sum_strength, cycle, x
            )

    return sum_strength


# Test cases
##########

t1 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 13140, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d10.txt")

# part 1 + 2

run_func(boom_part1, puzzle_input, DBG=False)

# PART 1 OK = 14060
# PART 2 OK = PAPKFKEJ
