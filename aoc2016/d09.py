# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func

# Main function
################


def get_size(line, recurse):
    idx = 0
    len_line = len(line)
    blowup_size = 0

    while idx < len_line:
        if line[idx] != "(":
            blowup_size += 1
            idx += 1
        else:
            jdx = line.find(")", idx)
            numbers = list(map(int, re.findall(r"-?\d+", line[idx:jdx])))
            size = numbers[0]
            times = numbers[1]
            if recurse:
                blowup_size += times * get_size(
                    line[jdx + 1 : jdx + 1 + size], True  # noqa
                )  # noqa
            else:
                blowup_size += times * size

            idx = jdx + size + 1

    return blowup_size


def boom_part1(input_val, DBG=True):
    return get_size(input_val[0], False)


def boom_part2(input_val, DBG=True):
    return get_size(input_val[0], True)


# Test cases
#############


t1 = "ADVENT"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 6, True)

t1 = "A(1x5)BC"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 7, True)

t1 = "(3x3)XYZ"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 9, True)

t1 = "A(2x2)BCD(2x2)EFG"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 11, True)

t1 = "(6x1)(1x3)A"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 6, True)

t1 = "X(8x2)(3x3)ABCY"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 18, True)

# quit()


t1 = "(3x3)XYZ"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 9, True)

t1 = "X(8x2)(3x3)ABCY"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 20, True)

t1 = "(27x12)(20x12)(13x14)(7x10)(1x12)A"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 241920, True)

t1 = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 445, True)

# quit()

# Real data
############

puzzle_input = read_input_file("input-d09.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 150914
# PART 2 OK = 11052855125
