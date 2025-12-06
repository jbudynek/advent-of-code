import portion as P

ipt_test = """3-5
10-14
16-20
12-18

1
5
8
11
17
32""".split("\n\n") # fmt: skip

ipt_puzzle = open("input.txt").read().split("\n\n")

ipt = ipt_puzzle

# ipt = ipt_test

itvs = [tuple(map(int, itv.split("-"))) for itv in ipt[0].splitlines()]

res1 = sum(
    1
    for ing in map(int, ipt[1].splitlines())
    if any(itv[0] <= ing <= itv[1] for itv in itvs)
)

all_intervals = P.empty()
for itv in itvs:
    all_intervals = all_intervals | P.closed(itv[0], itv[1])

res2 = sum(p.upper - p.lower + 1 for p in all_intervals)

print(f"# Part 1 solution: {res1}")
print(f"# Part 2 solution: {res2}")

# Part 1 solution: 707
# Part 2 solution: 361615643045059
