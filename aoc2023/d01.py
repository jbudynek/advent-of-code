# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


def boom_part1(input_val, DBG=True):
    calibration_total = 0
    digits_in_line = []
    for line in input_val:
        digits_in_line = []
        for cc in line:
            if cc in "1234567890":
                digits_in_line.append((cc))
        calibration_total += int(digits_in_line[0] + digits_in_line[-1])
    return calibration_total


def boom_part2(input_val, DBG=True):
    digit_to_digit = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    calibration_total = 0
    digits_in_line = []
    for line in input_val:
        digits_in_line = []
        for i in range(len(line)):
            for k, v in digit_to_digit.items():
                if line[i:].startswith(k):
                    digits_in_line.append(v)
        if DBG:
            print(digits_in_line)
        calibration_total += int(digits_in_line[0] + digits_in_line[-1])
    return calibration_total


# Test cases
#############


t1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 142, True)

t1 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
tt1 = t1.splitlines()

test_func(boom_part2, tt1, 281, True)

# Real data
############

puzzle_input = read_input_file("input.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 54632
# Part 2 solution: 54019
