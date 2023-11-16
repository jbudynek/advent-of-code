# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# Main function
################


def parse_input(input_val):
    variables = {}
    program = []
    for line in input_val:
        ss = line.split(" ")
        if ss[0] not in variables:
            variables[ss[0]] = 0
        program.append(
            " ".join(ss[3:]) + ": " + ss[0] + ("+=" if "inc" in ss[1] else "-=") + ss[2]
        )
    return program, variables


def get_max(variables):
    return max([val for val in variables.values() if isinstance(val, int)])


def boom_part1(input_val, DBG=True):
    program, variables = parse_input(input_val)
    exec("\n".join(program), variables)
    ret = get_max(variables)
    return ret


def boom_part2(input_val, DBG=True):
    program, variables = parse_input(input_val)
    ret = 0
    for line in program:
        exec(line, variables)
        ret = max(ret, get_max(variables))
    return ret


# Test cases
#############


t1 = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 1, True)
test_func(boom_part2, tt1, 10, True)

# Real data
############

puzzle_input = read_input_file("input-d08.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 6343
# PART 2 OK = 7184
