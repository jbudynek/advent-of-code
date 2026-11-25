# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# Codes are written along diagonals; code number n (1-based) is
# 20151125 * 252533^(n-1) mod 33554393.
# - Position -> index: cell (row r, column c) lies on diagonal d = r + c - 1.
#   The d-1 previous diagonals hold d*(d-1)/2 cells, and within diagonal d the
#   cell is the c-th one (the diagonal goes up and to the right, starting at
#   column 1), so n = d*(d-1)/2 + c.
# - Part 1: compute n for the puzzle's (row, column) and use fast modular
#   exponentiation (pow with a modulus) instead of looping n times.
# - Part 2: no computation; the puzzle only asks for the 49 other stars, so there
#   is nothing to solve or submit.

ipt_puzzle = open("input.txt").read().strip()

START = 20151125
FACTOR = 252533
MOD = 33554393


def parse(ipt):
    nums = [int(x.strip(".,")) for x in ipt.split() if x.strip(".,").isdigit()]
    return nums[0], nums[1]


def code(row, col):
    d = row + col - 1
    n = d * (d - 1) // 2 + col
    return START * pow(FACTOR, n - 1, MOD) % MOD


# test: cells from the puzzle's grid
assert code(1, 1) == 20151125
assert code(2, 1) == 31916031
assert code(1, 2) == 18749137
assert code(3, 4) == 7981243
assert code(4, 2) == 32451966
assert code(6, 6) == 27995004
print("# Test part 1: grid cells match")

r1 = code(*parse(ipt_puzzle))
print(f"# Part 1 solution: {r1}")

# Part 1 solution: 8997277
# Part 2 solution: none (no puzzle; requires collecting the 49 other stars)
