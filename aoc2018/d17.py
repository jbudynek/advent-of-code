# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model)
# Part 1: Parse clay veins and simulate downward/sideways water flow with a stack,
# counting every reached tile within the clay scan's vertical range.
# Part 2: Count only tiles converted to settled water (~), which remain after
# transient flowing water has drained.

import re
import sys

sys.setrecursionlimit(10000)


ipt_test = '''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''
ipt_puzzle = open("input.txt").read().strip()


def parse_scan(text):
    clay = set()
    for line in text.splitlines():
        numbers = [int(value) for value in re.findall(r"\d+", line)]
        if line.startswith("x="):
            x, y1, y2 = numbers
            for y in range(y1, y2 + 1):
                clay.add((x, y))
        else:
            y, x1, x2 = numbers
            for x in range(x1, x2 + 1):
                clay.add((x, y))
    return clay


def simulate(text):
    clay = parse_scan(text)
    max_y = max(y for _, y in clay)
    min_y = min(y for _, y in clay)
    flowing = set()
    settled = set()

    def blocked(x, y):
        return (x, y) in clay or (x, y) in settled

    def fill(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if cy > max_y or (cx, cy) in clay or (cx, cy) in settled:
                continue

            while cy <= max_y and not blocked(cx, cy):
                flowing.add((cx, cy))
                cy += 1
            if cy > max_y:
                continue

            cy -= 1
            left_open = False
            right_open = False

            lx = cx
            while not blocked(lx, cy):
                if not blocked(lx, cy + 1):
                    left_open = True
                    break
                lx -= 1

            rx = cx
            while not blocked(rx, cy):
                if not blocked(rx, cy + 1):
                    right_open = True
                    break
                rx += 1

            if not left_open and not right_open:
                for sx in range(lx + 1, rx):
                    settled.add((sx, cy))
                    flowing.discard((sx, cy))
                if cy - 1 >= 0:
                    stack.append((cx, cy - 1))
            else:
                lx = cx
                while not blocked(lx, cy):
                    flowing.add((lx, cy))
                    if not blocked(lx, cy + 1):
                        break
                    lx -= 1
                rx = cx
                while not blocked(rx, cy):
                    flowing.add((rx, cy))
                    if not blocked(rx, cy + 1):
                        break
                    rx += 1

                if left_open:
                    stack.append((lx, cy))
                if right_open:
                    stack.append((rx, cy))

    fill(500, 0)
    reached = {(x, y) for x, y in flowing | settled if min_y <= y <= max_y}
    return len(reached), len(settled)


def part1(text):
    return simulate(text)[0]


def part2(text):
    return simulate(text)[1]


example_answers = simulate(ipt_test)
assert example_answers == (57, 29)

if __name__ == "__main__":
    part1_answer, part2_answer = simulate(ipt_puzzle)
    print(part1_answer)
    print(part2_answer)


# Part 1: 38021
# Part 2: 32069