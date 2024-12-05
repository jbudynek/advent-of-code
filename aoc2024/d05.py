ipt = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

ipt = open("input.txt").read()

lines = ipt.split("\n")
rules, to_print = [], []
for line in lines:
    if "|" in line:
        rules.append([int(e) for e in line.split("|")])
    elif "," in line:
        to_print.append([int(e) for e in line.split(",")])


def validate_line(tp, rules):
    for [lhs, rhs] in rules:
        if (lhs not in tp) or (rhs not in tp):
            continue
        li = list(tp).index(lhs)
        ri = list(tp).index(rhs)
        if not (li < ri):
            return False
    return True


def reorder_line(tp, rules):
    change = True
    while change:
        change = False
        for [lhs, rhs] in rules:
            if (lhs not in tp) or (rhs not in tp):
                continue
            li = list(tp).index(lhs)
            ri = list(tp).index(rhs)
            if not (li < ri):
                tp[li], tp[ri] = tp[ri], tp[li]
                change = True
    return tp


result1, result2 = 0, 0
for tp in to_print:
    if validate_line(tp, rules):
        result1 += int(tp[len(tp) // 2])
    else:
        tp2 = reorder_line(tp, rules)
        result2 += int(tp2[len(tp2) // 2])

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 4814
# Part 2 solution: 5448
