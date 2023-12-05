# coding: utf-8
from boilerplate import read_input_file, run_func, test_func

# note: I wrote the code for part one on my phone in a colab notebook =)


def parse_rules(ipt, DBG):
    seeds = []
    s2s, s2f, f2w, w2l, l2t, t2h, h2l, mapp = [], [], [], [], [], [], [], []
    for line in ipt:
        if line == "":
            continue
        elif line.startswith("seed-"):
            mapp = s2s
            continue
        elif line.startswith("soil-"):
            mapp = s2f
            continue
        elif line.startswith("fertilizer-"):
            mapp = f2w
            continue
        elif line.startswith("water"):
            mapp = w2l
            continue
        elif line.startswith("light"):
            mapp = l2t
            continue
        elif line.startswith("temperature"):
            mapp = t2h
            continue
        elif line.startswith("humidity"):
            mapp = h2l
            continue
        elif line.startswith("seeds"):
            ss = line.split(":")
            seeds = [int(s) for s in ss[1].split()]
            if DBG:
                print(seeds)
            continue
        mapp.append([int(s) for s in line.split()])

    if DBG:
        print(s2s)
    if DBG:
        print(h2l)

    return seeds, s2s, s2f, f2w, w2l, l2t, t2h, h2l


def n(mapp, v):
    for line in mapp:
        d = line[0]
        s = line[1]
        r = line[2]
        if v >= s and v < s + r:
            return d + v - s
    return v


def rev_n(mapp, v):
    for line in mapp:
        d = line[0]
        s = line[1]
        r = line[2]
        if v >= d and v < d + r:
            return s + v - d
    return v


def chain(s, s2s, s2f, f2w, w2l, l2t, t2h, h2l):
    p1 = n(s2s, s)
    p2 = n(s2f, p1)
    p3 = n(f2w, p2)
    p4 = n(w2l, p3)
    p5 = n(l2t, p4)
    p6 = n(t2h, p5)
    p7 = n(h2l, p6)
    return p7


def rev_chain(s, s2s, s2f, f2w, w2l, l2t, t2h, h2l):
    p7 = rev_n(h2l, s)
    p6 = rev_n(t2h, p7)
    p5 = rev_n(l2t, p6)
    p4 = rev_n(w2l, p5)
    p3 = rev_n(f2w, p4)
    p2 = rev_n(s2f, p3)
    p1 = rev_n(s2s, p2)
    return p1


def val_in_seeds(val, seeds):
    idx = 0
    while idx < len(seeds):
        s0 = seeds[idx]
        s1 = seeds[idx + 1]
        if val >= s0 and val < s0 + s1:
            return True
        idx += 2
    return False


# Main function
################


def boom_part1(input_val, DBG=True):
    seeds, s2s, s2f, f2w, w2l, l2t, t2h, h2l = parse_rules(input_val, DBG)
    ret = []
    for s in seeds:
        p7 = chain(s, s2s, s2f, f2w, w2l, l2t, t2h, h2l)
        ret.append(p7)
        if DBG:
            print(min(ret))
    if DBG:
        print("**", min(ret))
    return min(ret)


# find where to start and work in reverse
def boom_part2(input_val, DBG=True):
    seeds, s2s, s2f, f2w, w2l, l2t, t2h, h2l = parse_rules(input_val, DBG)
    ret = []

    idx = 0
    while idx < len(seeds):
        s0 = seeds[idx]
        s1 = seeds[idx + 1]
        lhs = s0
        rhs = s0 + s1 - 1
        p7_l = chain(lhs, s2s, s2f, f2w, w2l, l2t, t2h, h2l)
        p7_r = chain(rhs, s2s, s2f, f2w, w2l, l2t, t2h, h2l)
        ret.append(p7_l)
        ret.append(p7_r)
        if DBG:
            print("*", min(ret))
        idx += 2
    if DBG:
        print("**", min(ret))

    idx = min(ret) // 3
    while True:
        val = rev_chain(idx, s2s, s2f, f2w, w2l, l2t, t2h, h2l)
        if DBG:
            print(val)

        if val_in_seeds(val, seeds):
            return idx
        else:
            idx += 1


# Test cases
#############


t1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 35, True)
test_func(boom_part2, tt1, 46, True)

# Real data
############

puzzle_input = read_input_file("input-d05.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

quit()

# Part 1 solution: 388071289
# Part 2 solution: 84206669
