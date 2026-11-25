# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# Two linear congruential generators: value = value * factor % 2147483647, with
# factor 16807 for A and 48271 for B, starting from the puzzle input values.
# - Part 1: run 40 million steps; each step, compare the lowest 16 bits of both
#   new values (x & 0xFFFF) and count the matches. Pure simulation, no memory
#   needed since only the current values are kept.
# - Part 2: same generators, but each one only hands over values that are multiples
#   of 4 (A) or 8 (B): a generator keeps stepping until its value qualifies. The
#   k-th accepted value of A is compared with the k-th accepted value of B, for
#   5 million pairs. Same simulation with an inner "advance until multiple" loop.

ipt_test = """Generator A starts with 65
Generator B starts with 8921"""

ipt_puzzle = open("input.txt").read().strip()

MOD = 2147483647
FA = 16807
FB = 48271


def parse(ipt):
    a, b = [int(line.split()[-1]) for line in ipt.splitlines()]
    return a, b


def judge(a, b, n=40_000_000):
    count = 0
    for _ in range(n):
        a = a * FA % MOD
        b = b * FB % MOD
        if (a ^ b) & 0xFFFF == 0:
            count += 1
    return count


def judge2(a, b, n=5_000_000):
    count = 0
    for _ in range(n):
        a = a * FA % MOD
        while a % 4:
            a = a * FA % MOD
        b = b * FB % MOD
        while b % 8:
            b = b * FB % MOD
        if (a ^ b) & 0xFFFF == 0:
            count += 1
    return count


# test
r_test1 = judge(*parse(ipt_test))
print(f"# Test part 1: {r_test1} (expected 588)")
r_test2 = judge2(*parse(ipt_test))
print(f"# Test part 2: {r_test2} (expected 309)")
assert r_test1 == 588
assert r_test2 == 309

r1 = judge(*parse(ipt_puzzle))
r2 = judge2(*parse(ipt_puzzle))
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 592
# Part 2 solution: 320
