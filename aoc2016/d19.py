# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: This is the Josephus problem with k=2. Simulate with a deque: the
# elf at the front steals from the next one (which is dropped), then moves to
# the back of the queue. The last elf remaining wins. O(n).
#
# Part 2: The victim is the elf across the circle. Split the circle into two
# deques: `left` (first half, holding the current thief at its front) and
# `right` (second half, whose front is always the elf across). Each round:
# pop the victim from the front of `right`, move the thief from the front of
# `left` to the back of `right`, then rebalance so that len(right) is
# len(left) or len(left)+1. Last remaining elf wins. O(n).

from collections import deque

ipt_test = "5"
ipt_puzzle = open("input.txt").read().strip()


def part1(n):
    q = deque(range(1, n + 1))
    while len(q) > 1:
        q.rotate(-1)
        q.popleft()
    return q[0]


def part2(n):
    left = deque(range(1, n // 2 + 1))
    right = deque(range(n // 2 + 1, n + 1))
    while len(left) + len(right) > 1:
        right.popleft()
        right.append(left.popleft())
        if len(right) - len(left) > 1:
            left.append(right.popleft())
    return (left or right)[0]


assert part1(int(ipt_test)) == 3
assert part2(int(ipt_test)) == 2

print("Part 1:", part1(int(ipt_puzzle)))
print("Part 2:", part2(int(ipt_puzzle)))

# Part 1 solution: 1816277
# Part 2 solution: 1410967
