import re
import numpy as np

ipt_test = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """.splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test

# Part 1

all_problems = {}
max_lin = len(ipt)
max_col = len(re.split(r"\s+", ipt[0].strip()))
for y, line in enumerate(ipt):
    nn = re.split(r"\s+", line.strip())
    for x, c in enumerate(nn):
        all_problems[(x, y)] = c

out1 = []
for col in range(max_col):
    op = all_problems[(col, max_lin - 1)]
    res1 = int(all_problems[(col, 0)])
    for lin in range(1, max_lin - 1):
        rhs = int(all_problems[(col, lin)])
        if op == "*":
            res1 *= rhs
        else:
            res1 += rhs
    out1.append(res1)

# part 2

matrix = np.array([list(line) for line in ipt])

transposed = matrix.T

out2 = []
res2 = -1
op = ""
for idx_row in range(transposed.shape[0]):
    line = "".join(transposed[idx_row, :]).strip()
    if line == "":
        out2.append(res2)
        res2 = -1
        op = ""
    else:
        if line[-1] == "*":
            op = "*"
            line = line[:-1]
        elif line[-1] == "+":
            op = "+"
            line = line[:-1]
        rhs = int(line)
        if res2 == -1:
            res2 = rhs
        else:
            if op == "*":
                res2 *= rhs
            else:
                res2 += rhs

out2.append(res2)

print(f"# Part 1 solution: {sum(out1)}")
print(f"# Part 2 solution: {sum(out2)}")

# Part 1 solution: 4309240495780
# Part 2 solution: 9170286552289
