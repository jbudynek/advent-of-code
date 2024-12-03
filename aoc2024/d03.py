import re

# ipt="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
# ipt="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
ipt = open("input.txt").read()

muls = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don\'t\(\))", ipt)

do = True

out1 = []
out2 = []
for m in muls:
    if m[2] == "don't()":
        do = False
    elif m[1] == "do()":
        do = True
    else:
        ii = list(map(int, re.findall(r"-?\d+", m[0])))
        out1.append(ii[0] * ii[1])
        if do:
            out2.append(ii[0] * ii[1])

result1 = sum(out1)
result2 = sum(out2)

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 190604937
# Part 2 solution: 82857512
