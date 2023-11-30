# coding: utf-8

from boilerplate import read_input_file, run_func, test_func

# Main function
################


def boom_part1(input_val, DBG=True):
    return -1


def boom_part2(input_val, DBG=True):
    return -1


# Test cases
#############


t1 = "3,4,3,1,2"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, -1, True)
test_func(boom_part2, tt1, -1, True)
# quit()

# Real data
############

puzzle_input = read_input_file("input-d11.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution:
# Part 2 solution:
