# coding: utf-8
import functools
from collections import Counter

from boilerplate import read_input_file, run_func, test_func


def get_strength(n0, n1, nj):
    if n0 + nj == 5:
        return 7
    if n0 + nj == 4:
        return 6
    if (n0 + nj == 3 and n1 == 2) or (n0 == 3 and n1 + nj == 2):
        return 5
    if n0 + nj == 3:
        return 4
    if (n0 + nj == 2 and n1 == 2) or (n0 == 2 and n1 + nj == 2):
        return 3
    if n0 + nj == 2:
        return 2
    if n0 + nj == 1:
        return 1
    return 0


def hand_strength(h, with_joker):
    c = Counter(h)
    nj = 0
    if with_joker:
        nj = c["J"]
        del c["J"]
    mc = c.most_common()
    n0 = 0 if len(mc) == 0 else mc[0][1]
    n1 = 0 if len(mc) <= 1 else mc[1][1]
    return get_strength(n0, n1, nj)


def boom_all(ipt, with_joker):

    order_1 = "AKQJT98765432"
    order_2 = "AKQT98765432J"

    cards_order = order_2 if with_joker else order_1

    hand2bid = {line.split()[0]: int(line.split()[1]) for line in ipt}

    hands = hand2bid.keys()

    def compare_hands(lhs, rhs):
        ls = hand_strength(lhs, with_joker)
        rs = hand_strength(rhs, with_joker)
        if ls != rs:
            return rs - ls
        for i in range(len(lhs)):
            r = cards_order.find(lhs[i]) - cards_order.find(rhs[i])
            if r != 0:
                return r

    hands = reversed(sorted(hands, key=functools.cmp_to_key(compare_hands)))

    ans = 0
    for i, h in enumerate(hands):
        ans += hand2bid[h] * (i + 1)
    return ans


def boom_part1(ipt, DBG=True):
    return boom_all(ipt, False)


def boom_part2(ipt, DBG=True):
    return boom_all(ipt, True)


# Test cases
#############


ipt_test1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()
test_func(boom_part1, ipt_test1, 6440, True)
test_func(boom_part2, ipt_test1, 5905, True)
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

# Part 1 solution: 250347426
# Part 2 solution: 251224870
