import re

# ipt="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
# ipt="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
ipt = open("input.txt").read()

muls = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don\'t\(\))", ipt)

factor = 1
products, factors = [], []
for mul, do, dont in muls:
    if dont == "don't()" or do == "do()":
        factor = 1 - factor
    else:
        ii = list(map(int, re.findall(r"-?\d+", mul)))
        products.append(ii[0] * ii[1])
        factors.append(factor)

print(f"# Part 1 solution: {sum(products)}")
print(f"# Part 2 solution: {sum([p * f for p, f in zip(products, factors)])}")


# Part 1 solution: 190604937
# Part 2 solution: 82857512
