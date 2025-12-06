ipt_test = """ne,ne,s,s"""

ipt_puzzle = open("input.txt").read().strip()

# ipt=ipt_test
ipt = ipt_puzzle

delta = {
    "n": (0 + 2j),
    "s": (0 - 2j),
    "ne": (1 + 1j),
    "se": (1 - 1j),
    "nw": (-1 + 1j),
    "sw": (-1 - 1j),
}


def steps(z):
    return int(abs(z.real)) + int(abs(z.imag) - abs(z.real)) // 2


z = 0 + 0j

max_steps = 0

for step in ipt.split(","):
    z += delta[step]
    max_steps = max(max_steps, steps(z))

r1 = steps(z)
r2 = max_steps

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 715
# Part 2 solution: 1512
