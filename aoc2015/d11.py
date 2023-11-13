# coding: utf-8
import string
from functools import reduce

from boilerplate import run_func, test_func

# Main function
##########


def divmod_26(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b


def to_26(num):
    chars = []
    while num > 0:
        num, d = divmod_26(num)
        chars.append(string.ascii_lowercase[d - 1])
    return "".join(reversed(chars))


def from_26(chars):
    return reduce(
        lambda r, x: r * 26 + x + 1, map(string.ascii_lowercase.index, chars), 0
    )


def is_valid(start_10, DBG=False):
    start_26 = to_26(start_10)
    # abc ... xyz
    contains = False
    for i in range(24):
        cc = to_26(from_26("abc") + i * from_26("aaa"))
        if cc in start_26:
            contains = True
            break
    if not contains:
        return False

    if "i" in start_26:
        return False
    if "o" in start_26:
        return False
    if "l" in start_26:
        return False

    count_double = 0
    for i in range(26):
        cc = to_26(from_26("aa") + i * from_26("aa"))
        if cc in start_26:
            count_double += 1
            if count_double == 2:
                break

    if count_double < 2:
        return False

    return True


def boom_part1(input_val, DBG=True):

    start = from_26(input_val)
    start = start + 1

    while not is_valid(start, DBG):
        start = start + 1

    return to_26(start)


def boom_part2(input_val, DBG=True):

    return boom_part1(input_val, DBG)


# Test cases
##########

test_func(boom_part1, "abcdefgh", "abcdffaa", True)
test_func(boom_part1, "ghijklmn", "ghjaabcc", True)

# Real data
##########

puzzle_input = "vzbxkghb"

# part 1
run_func(boom_part1, puzzle_input, DBG=False)

# part 2

puzzle_input = "vzbxxyzz"

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = vzbxxyzz
# PART 2 OK = vzcaabcc
