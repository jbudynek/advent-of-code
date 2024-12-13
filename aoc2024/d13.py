import re

import numpy as np

ipt = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".split(
    "\n\n"
)

ipt = open("input.txt").read().split("\n\n")


def solve(a1, b1, a2, b2, c1, c2):
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])

    solution = np.linalg.solve(A, B)

    sa = int(np.round(solution[0]))
    sb = int(np.round(solution[1]))

    if (a1 * sa + b1 * sb == c1) and (a2 * sa + b2 * sb == c2):
        return 3 * sa + 1 * sb
    else:
        return 0


r1, r2 = 0, 0
for round in ipt:
    lines = round.split("\n")
    button_A = list(map(int, re.findall(r"-?\d+", lines[0])))
    button_B = list(map(int, re.findall(r"-?\d+", lines[1])))
    prize = list(map(int, re.findall(r"-?\d+", lines[2])))

    r1 += solve(button_A[0], button_B[0], button_A[1], button_B[1], prize[0], prize[1])
    r2 += solve(
        button_A[0],
        button_B[0],
        button_A[1],
        button_B[1],
        prize[0] + 10000000000000,
        prize[1] + 10000000000000,
    )


print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 39996
# Part 2 solution: 73267584326867
