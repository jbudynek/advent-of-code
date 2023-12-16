# coding: utf-8
from collections import OrderedDict, defaultdict

from boilerplate import read_input_file, run_func, test_func


def hash_algo(s):
    cv = 0
    i = 0
    while i < len(s):
        c = s[i]
        cv += ord(c)
        cv *= 17
        cv %= 256
        i += 1
    return cv


def boom_part1(ipt, DBG=True):
    line = ipt[0]
    ans = 0
    for inst in line.split(","):
        ans += hash_algo(inst)
    return ans


def process(inst, hashmap):
    label = ""
    if "=" in inst:
        s = inst.split("=")
        label = s[0]
        box_id = hash_algo(s[0])
        fl = int(s[1])
        dd = hashmap[box_id]
        dd[label] = fl
    elif "-" in inst:
        s = inst.split("-")
        label = s[0]
        box_id = hash_algo(s[0])
        dd = hashmap[box_id]
        if label in dd:
            del dd[label]


def boom_part2(ipt, DBG=True):
    line = ipt[0]
    hashmap = defaultdict(OrderedDict)
    for inst in line.split(","):
        process(inst, hashmap)

    ans = 0
    for k, v in hashmap.items():
        for id, vv in enumerate(v.values()):
            ans += (k + 1) * (id + 1) * vv

    return ans


# Test cases
#############

ipt_test1 = """HASH""".splitlines()
test_func(boom_part1, ipt_test1, 52, True)

ipt_test1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""".splitlines()
test_func(boom_part1, ipt_test1, 1320, True)
test_func(boom_part2, ipt_test1, 145, True)
# quit()

# Real data
############

ipt_puzzle = read_input_file("input.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 511257
# Part 2 solution: 239484
