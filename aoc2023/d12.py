# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

CACHE = {}  # type: ignore


def count_the_ways(line: str, counts: list[int]):

    kk = line + "_" + str(counts)
    if kk in CACHE:
        return CACHE[kk]

    if len(line) == 0 and len(counts) == 0:
        CACHE[kk] = 1
        return CACHE[kk]
    elif len(line) == 0 and len(counts) > 0:
        CACHE[kk] = 0
        return CACHE[kk]
    elif len(counts) == 0 and ("#" in line):
        CACHE[kk] = 0
        return CACHE[kk]
    elif line[0] == ".":
        CACHE[kk] = count_the_ways(line[1:], counts)
        return CACHE[kk]
    elif line[0] == "#":
        idx_dot = line.find(".")
        if idx_dot >= counts[0] and line[counts[0]] == "?":
            CACHE[kk] = count_the_ways(line[counts[0] + 1 :], counts[1:])  # noqa
            return CACHE[kk]
        elif idx_dot == counts[0]:
            CACHE[kk] = count_the_ways(line[counts[0] + 1 :], counts[1:])  # noqa
            return CACHE[kk]
        elif idx_dot == -1 and len(line) == counts[0] and len(counts) == 1:
            CACHE[kk] = 1
            return CACHE[kk]
        elif idx_dot == -1 and len(line) > counts[0] and line[counts[0]] == "?":
            CACHE[kk] = count_the_ways(line[counts[0] + 1 :], counts[1:])  # noqa
            return CACHE[kk]
        else:
            CACHE[kk] = 0
            return CACHE[kk]
    elif line[0] == "?":
        newline1 = "#" + line[1:]
        newline2 = "." + line[1:]
        c1 = count_the_ways(newline1, counts)
        c2 = count_the_ways(newline2, counts)
        CACHE[kk] = c1 + c2
        return CACHE[kk]
    else:
        raise (Exception("oops"))


def boom_part1(ipt, DBG=True):
    ans = 0
    for line in ipt:
        ss = line.split()
        counts = [int(x) for x in ss[1].split(",")]
        c0 = ss[0]
        ans += count_the_ways(c0, counts)

    return ans


def boom_part2(ipt, DBG=True):
    ans = 0
    for line in ipt:
        ss = line.split()
        counts = [int(x) for x in ss[1].split(",")] * 5
        c0 = ss[0] + ("?" + ss[0]) * 4
        ans += count_the_ways(c0, counts)

    return ans


# Test cases
#############

ipt_test1 = """???.### 1,1,3""".splitlines()
test_func(boom_part1, ipt_test1, 1, True)
test_func(boom_part2, ipt_test1, 1, True)

ipt_test1 = """.??..??...?##. 1,1,3""".splitlines()
test_func(boom_part1, ipt_test1, 4, True)
test_func(boom_part2, ipt_test1, 16384, True)

ipt_test1 = """?#?#?#?#?#?#?#? 1,3,1,6""".splitlines()
test_func(boom_part1, ipt_test1, 1, True)
test_func(boom_part2, ipt_test1, 1, True)

ipt_test1 = """????.#...#... 4,1,1""".splitlines()
test_func(boom_part1, ipt_test1, 1, True)
test_func(boom_part2, ipt_test1, 16, True)

ipt_test1 = """????.######..#####. 1,6,5""".splitlines()
test_func(boom_part1, ipt_test1, 4, True)
test_func(boom_part2, ipt_test1, 2500, True)

ipt_test1 = """?###???????? 3,2,1""".splitlines()
test_func(boom_part1, ipt_test1, 10, True)
test_func(boom_part2, ipt_test1, 506250, True)


ipt_test1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()
test_func(boom_part1, ipt_test1, 21, True)
test_func(boom_part2, ipt_test1, 525152, True)

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 7633
# Part 2 solution: 23903579139437
