ipt_test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

ipt_puzzle = open("input-d02.txt").read()

# ipt=ipt_test
ipt = ipt_puzzle


def validate(report):
    if not ((sorted(report) == report) or (list(reversed(sorted(report))) == report)):
        return False
    for idx in range(1, len(report)):
        delta = abs(report[idx] - report[idx - 1])
        if delta < 1 or delta > 3:
            return False
    return True


result1 = 0
result2 = 0
for line in ipt.split("\n"):
    report = [int(e) for e in line.split()]
    if validate(report):
        result1 += 1
    for idx in range(len(report)):
        report2 = report.copy()
        del report2[idx]
        if validate(report2):
            result2 += 1
            break

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 219
# Part 2 solution: 290
