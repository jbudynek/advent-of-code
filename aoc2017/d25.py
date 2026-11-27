# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Simulate the sparse infinite tape, applying the Turing-machine state rules
#   to the cursor for the requested number of steps and count remaining ones.

import re

ipt_test = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

ipt_puzzle = open("input.txt").read().strip()


def parse_blueprint(text):
    start = re.search(r"Begin in state ([A-Z])\.", text).group(1)
    steps = int(re.search(r"after (\d+) steps", text).group(1))
    rules = {}

    pattern = re.compile(
        r"In state ([A-Z]):(?:(?!\nIn state ).)*?"
        r"If the current value is 0:(.*?)"
        r"If the current value is 1:(.*?)(?=\nIn state |\Z)",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        state = match.group(1)
        state_rules = {}
        for value, body in ((0, match.group(2)), (1, match.group(3))):
            write = int(re.search(r"Write the value ([01])\.", body).group(1))
            move = re.search(r"Move one slot to the (left|right)", body).group(1)
            next_state = re.search(r"Continue with state ([A-Z])\.", body).group(1)
            state_rules[value] = (write, -1 if move == "left" else 1, next_state)
        rules[state] = state_rules

    return start, steps, rules


def diagnostic_checksum(text):
    state, steps, rules = parse_blueprint(text)
    tape = set()
    position = 0

    for _ in range(steps):
        value = 1 if position in tape else 0
        write, move, state = rules[state][value]
        if write:
            tape.add(position)
        else:
            tape.discard(position)
        position += move

    return len(tape)


# test
r_test1 = diagnostic_checksum(ipt_test)
print(f"# Test part 1: {r_test1} (expected 3)")
assert r_test1 == 3

r1 = diagnostic_checksum(ipt_puzzle)
print(f"# Part 1 solution: {r1}")

# Part 1 solution: 2870
