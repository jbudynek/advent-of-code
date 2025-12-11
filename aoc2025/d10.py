import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

ipt_test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test

machines = []
machines_bin = []
for line in ipt:
    parts = line.split(" ")
    target = parts[0][1:-1]
    target_bin = 0
    for d in reversed(target):
        target_bin *= 2
        if d == "#":
            target_bin += 1

    last = tuple(map(int, parts[-1][1:-1].split(",")))
    buttons = []
    buttons_bin = []
    for i in range(1, len(parts) - 1):
        buttons.append(list(map(int, parts[i][1:-1].split(","))))

    for b in buttons:
        b_bin = 0
        for d in b:
            b_bin += 2**d
        buttons_bin.append(b_bin)
    machines.append((target, buttons, last))
    machines_bin.append((target_bin, buttons_bin, last))


def apply(button, start):
    return button ^ start


def is_bit_set(p_int, n):
    return (p_int & (1 << n)) != 0


def process_machine(m_b):
    target_b = m_b[0]
    buttons_b = m_b[1]
    last_b = m_b[2]

    nb_buttons = len(buttons_b)

    mini = 1000
    for to_apply in range(2**nb_buttons):
        start = 0
        for n in range(nb_buttons):
            if is_bit_set(to_apply, n):
                start = apply(buttons_b[n], start)
        if start == target_b:
            cc = bin(to_apply).count("1")
            mini = min(mini, cc)

    return mini


def process_machine2(m):
    buttons = m[1]
    last = m[2]

    n_buttons = len(buttons)
    n_outputs = len(last)

    # Solve Ax = b with minimum constraint
    A = np.zeros((n_outputs, n_buttons))
    for i, button in enumerate(buttons):
        for idx in button:
            if idx < n_outputs:
                A[idx, i] = 1

    b = np.array(last)

    c = np.ones(n_buttons)
    constraints = LinearConstraint(A, b, b)
    bounds = Bounds(lb=0, ub=np.inf)
    integrality = np.ones(n_buttons)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    return int(round(result.fun))


out1 = []
for m_b in machines_bin:
    out1.append(process_machine(m_b))

out2 = []
for m in machines:
    out2.append(process_machine2(m))

print(f"# Part 1 solution: {sum(out1)}")
print(f"# Part 2 solution: {sum(out2)}")

# Part 1 solution: 428
# Part 2 solution: 16613
