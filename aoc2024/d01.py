ipt_test = """3   4
4   3
2   5
1   3
3   9
3   3"""

ipt_puzzle = open("input-d01.txt").read()

# ipt=ipt_test
ipt = ipt_puzzle

all_e = [int(e) for li in ipt.split("\n") for e in li.split()]

l1 = sorted(all_e[::2])
l2 = sorted(all_e[1::2])

r1 = [abs(e2 - e1) for (e1, e2) in zip(l1, l2)]
r2 = [e1 * l2.count(e1) for (e1, e2) in zip(l1, l2)]

print(f"# Part 1 solution: {sum(r1)}")
print(f"# Part 2 solution: {sum(r2)}")

# Part 1 solution: 2375403
# Part 2 solution: 23082277
