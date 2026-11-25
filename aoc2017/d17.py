# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# Spinlock on a circular buffer that starts as [0], current position 0.
# - Part 1: simulate directly with a Python list. For each value v in 1..2017,
#   move forward `step` positions (modulo the current length), insert v right
#   after that position, and make it the current position. At the end, return
#   the value located right after 2017 in the buffer (circularly).
# - Part 2: 50 million insertions is too many to store. But 0 always stays at
#   index 0, so the value after 0 is whatever was last inserted at index 1.
#   Only track the current position modulo the buffer length (which is just v
#   before inserting v): pos = (pos + step) % v + 1. Whenever pos == 1, record v.

ipt_test = "3"

ipt_puzzle = open("input.txt").read().strip()


def spin(step, n=2017):
    buf = [0]
    pos = 0
    for v in range(1, n + 1):
        pos = (pos + step) % len(buf) + 1
        buf.insert(pos, v)
    return buf[(buf.index(n) + 1) % len(buf)]


def spin2(step, n=50_000_000):
    pos = 0
    after_zero = None
    for v in range(1, n + 1):
        pos = (pos + step) % v + 1
        if pos == 1:
            after_zero = v
    return after_zero


# test
r_test1 = spin(int(ipt_test))
print(f"# Test part 1: {r_test1} (expected 638)")
assert r_test1 == 638

# test part 2: from the puzzle's example (step 3), after 9 insertions: 0 (9) 5 ...
assert spin2(int(ipt_test), 9) == 9

r1 = spin(int(ipt_puzzle))
print(f"# Part 1 solution: {r1}")
r2 = spin2(int(ipt_puzzle))
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1670
# Part 2 solution: 2316253
