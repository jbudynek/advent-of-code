ipt_test = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle


def find_max_digit(cur_line, reserve):
    max_digit = max(cur_line[: len(cur_line) - reserve + 1])
    idx_max_digit = cur_line.index(max_digit)
    return int(max_digit), idx_max_digit


def find_joltage(cur_line, nb_digits):
    joltage = 0
    for reserve in range(nb_digits, 0, -1):
        joltage *= 10
        digit, idx = find_max_digit(cur_line, reserve)
        cur_line = cur_line[idx + 1 :]
        joltage += digit
    return joltage


out1 = [find_joltage(line, 2) for line in ipt]
out2 = [find_joltage(line, 12) for line in ipt]

print(f"# Part 1 solution: {sum(out1)}")
print(f"# Part 2 solution: {sum(out2)}")

# Part 1 solution: 17034
# Part 2 solution: 168798209663590
