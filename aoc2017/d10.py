import re
from functools import reduce

ipt_test = """3, 4, 1, 5"""

ipt_puzzle = open("input.txt").read()

# ipt=ipt_test

ipt = ipt_puzzle

r1 = 0
r2 = 0
LEN = 256

lengths = list(map(int, re.findall(r"-?\d+", ipt)))
q = list(range(LEN))
idx = 0
idx2 = 0
skip = 0


def run_round(q, idx, idx2, skip):
    for l in lengths:
        q[idx : idx + l] = reversed(q[idx : idx + l])
        idx += l
        idx += skip
        idx2 += l
        idx2 += skip
        idx = idx % LEN
        skip += 1
        q = q[idx:] + q[:idx]
        idx = 0
    return q, idx, idx2, skip


q, idx, idx2, skip = run_round(q, idx, idx2, skip)

r1 = q[-idx2 % LEN] * q[-idx2 % LEN + 1]

# Part 2

ipt_test = """AoC 2017"""

# ipt = ipt_test
ipt = ipt_puzzle.strip()

lengths = [ord(c) for c in ipt] + [17, 31, 73, 47, 23]

q = list(range(LEN))

idx = 0
idx2 = 0
skip = 0

for i in range(64):
    q, idx, idx2, skip = run_round(q, idx, idx2, skip)

q = q[-idx2 % LEN :] + q[: -idx2 % LEN]

ret = ""
for i in range(16):
    l = q[i * 16 : (i + 1) * 16]
    x = reduce(lambda x, y: x ^ y, l)
    ret += format(x, "02x")

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {ret}")

# Part 1 solution: 40132
# Part 2 solution: 35b028fe2c958793f7d5a61d07a008c8
