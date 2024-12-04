# We use a 3-parts regular expression with capturing groups to get all 'mul's,
# 'do's and 'dont's. Then we iterate on them and store the results of the
# multiplications.
# A trick is to store a multiplying factor (which can be 0 or 1, and is
# switched (by using 1-x) every time we encounter a 'do' or a 'dont') to
# compute the second result.

import re

# ipt="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
# ipt="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
ipt = open("input.txt").read()

muls = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don\'t\(\))", ipt)

factor = 1
products, factors = [], []
for mul, do, dont in muls:
    if dont != "" or do != "":
        factor = 1 - factor
    else:
        ii = list(map(int, re.findall(r"-?\d+", mul)))
        products.append(ii[0] * ii[1])
        factors.append(factor)

print(f"# Part 1 solution: {sum(products)}")
print(f"# Part 2 solution: {sum([p * f for p, f in zip(products, factors)])}")


# Part 1 solution: 190604937
# Part 2 solution: 82857512
