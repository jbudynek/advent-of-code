# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Sort the blocked ranges by start and sweep through them keeping
# `nxt`, the lowest IP not yet known to be blocked. If a range starts after
# `nxt`, then `nxt` is allowed; otherwise push `nxt` past the range's end.
#
# Part 2: Same sweep, but every time a range starts after `nxt`, the gap
# [nxt, lo - 1] is allowed, so add its size to the count. After the last range,
# the tail [nxt, max_ip] is also allowed.

ipt_test = """5-8
0-2
4-7"""
ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    return sorted(tuple(map(int, line.split("-"))) for line in ipt.splitlines())


def part1(ipt):
    nxt = 0
    for lo, hi in parse(ipt):
        if lo > nxt:
            break
        nxt = max(nxt, hi + 1)
    return nxt


def part2(ipt, max_ip=4294967295):
    nxt = 0
    count = 0
    for lo, hi in parse(ipt):
        if lo > nxt:
            count += lo - nxt
        nxt = max(nxt, hi + 1)
    return count + max(0, max_ip + 1 - nxt)


assert part1(ipt_test) == 3
assert part2(ipt_test, 9) == 2

print("Part 1:", part1(ipt_puzzle))
print("Part 2:", part2(ipt_puzzle))

# Part 1 solution: 31053880
# Part 2 solution: 117
