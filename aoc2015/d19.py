# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# Main function
################


def parse_rules(input_val):
    compound = input_val[-1]
    del input_val[-1]
    del input_val[-1]
    inputs = []
    outputs = []
    for line in input_val:
        ss = line.split()
        inputs.append(ss[0])
        outputs.append(ss[2])

    return inputs, outputs, compound


def boom_part1(input_val, DBG=True):
    inputs, outputs, compound = parse_rules(input_val.copy())

    transform = set()
    c_idx = 0
    while c_idx < len(compound):
        for in_idx in range(len(inputs)):
            if compound[c_idx:].startswith(inputs[in_idx]):
                tr = compound[:c_idx] + compound[c_idx:].replace(
                    inputs[in_idx], outputs[in_idx], 1
                )
                transform.add(tr)
        c_idx += 1

    return len(transform)


def boom_part2(input_val, DBG=True):
    inputs, outputs, compound = parse_rules(input_val.copy())

    round_id = 0
    while compound != "e":
        if DBG:
            print(compound)
        for idx in range(len(inputs)):
            if outputs[idx] in compound:
                # replace last match
                compound = inputs[idx].join(compound.rsplit(outputs[idx], 1))
                round_id += 1
    return round_id


# Test cases
#############


t1 = """H => HO
H => OH
O => HH

HOHOHO"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 7, True)

t1 = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""
tt1 = t1.splitlines()
# test_func(boom_part2, tt1, 3, True)

t1 = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""
tt1 = t1.splitlines()
# test_func(boom_part2, tt1, 6, True)

# Real data
############

puzzle_input = read_input_file("input-d19.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 518
# PART 2 OK = 200
