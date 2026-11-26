# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: simulate each scrambling operation on a list of characters, in order.
# Rotate/swap/reverse/move are straightforward list operations; "rotate based on
# position of letter X" uses the index of X before rotating.
# Part 2: the rotate-based-on-position operation is awkward to invert, so instead
# brute-force all 8! = 40320 permutations of "abcdefgh" and find the one whose
# scrambled form is "fbgdceah".

from itertools import permutations

ipt_test = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""
ipt_puzzle = open("input.txt").read().strip()


def rot_right(s, k):
    k %= len(s)
    return s[-k:] + s[:-k] if k else s


def scramble(pw, ipt):
    s = list(pw)
    for line in ipt.splitlines():
        w = line.split()
        if w[0] == "swap" and w[1] == "position":
            x, y = int(w[2]), int(w[5])
            s[x], s[y] = s[y], s[x]
        elif w[0] == "swap":
            x, y = s.index(w[2]), s.index(w[5])
            s[x], s[y] = s[y], s[x]
        elif w[0] == "rotate" and w[1] == "based":
            i = s.index(w[6])
            s = rot_right(s, 1 + i + (1 if i >= 4 else 0))
        elif w[0] == "rotate":
            k = int(w[2])
            s = rot_right(s, k if w[1] == "right" else -k)
        elif w[0] == "reverse":
            x, y = int(w[2]), int(w[4])
            s[x:y + 1] = s[x:y + 1][::-1]
        elif w[0] == "move":
            x, y = int(w[2]), int(w[5])
            c = s.pop(x)
            s.insert(y, c)
    return "".join(s)


assert scramble("abcde", ipt_test) == "decab"
print(scramble("abcdefgh", ipt_puzzle))


def unscramble(target, ipt):
    for p in permutations("abcdefgh"):
        pw = "".join(p)
        if scramble(pw, ipt) == target:
            return pw


assert unscramble(scramble("abcdefgh", ipt_puzzle), ipt_puzzle) == "abcdefgh"
print(unscramble("fbgdceah", ipt_puzzle))

# Part 1 solution: baecdfgh
# Part 2 solution: cegdahbf
