# coding: utf-8
import sys

from boilerplate import read_input_file, run_func, test_func


def snafu_to_int(snafu: str):
    ret = 0
    for i, c in enumerate(reversed(snafu)):
        base = 5**i
        mult = 1
        if c == "-":
            mult = -1
        elif c == "=":
            mult = -2
        else:
            mult = int(c)
        ret += mult * base

    return ret


def int_to_snafu(n: int):
    ret = ""
    while n != 0:
        m = n % 5
        if m <= 2:
            ret = str(m) + ret
            n = n // 5
        elif m == 3:
            ret = "=" + ret
            n = (n // 5) + 1
        elif m == 4:
            ret = "-" + ret
            n = (n // 5) + 1

    return ret


def boom_part1(input_val, DBG=True):
    return int_to_snafu(sum(snafu_to_int(line) for line in input_val))


# Test cases
##########

t1 = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, "2=-1=0", True)

# Real data
##########

puzzle_input = read_input_file("input-d25.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")

sys.exit()

# PART 1 OK = 2--2-0=--0--100-=210
