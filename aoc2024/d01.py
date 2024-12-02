with open("input-d01.txt", "r") as file:
    ipt_puzzle = file.read()

ipt_test = """3   4
4   3
2   5
1   3
3   9
3   3"""

# ipt=ipt_test
ipt = ipt_puzzle

lines = [li for li in ipt.split("\n")]

l1 = []
l2 = []
for li in lines:
    if li == "":
        continue
    [e1, e2] = li.split()
    l1.append(int(e1))
    l2.append(int(e2))

l1 = sorted(l1)
l2 = sorted(l2)

r1 = [abs(e2 - e1) for (e1, e2) in zip(l1, l2)]
r2 = [e1 * l2.count(e1) for (e1, e2) in zip(l1, l2)]

result1 = sum(r1)
result2 = sum(r2)

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 2375403
# Part 2 solution: 23082277
