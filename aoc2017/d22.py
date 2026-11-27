# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: use a sparse set for infected nodes and turn a carrier left or
#   right according to whether its current node is infected, toggling it.
# - Part 2: track clean, weakened, infected, and flagged nodes with a sparse
#   state dictionary, applying the evolved left/straight/right/reverse turns.

ipt_test = """..#
#..
..."""

ipt_puzzle = open("input.txt").read().strip()


def infected_count(text, bursts):
    rows = text.splitlines()
    size = len(rows)
    infected = {
        (row, col)
        for row, line in enumerate(rows)
        for col, value in enumerate(line)
        if value == "#"
    }
    position = (size // 2, size // 2)
    direction = 0  # up, right, down, left
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    infections = 0

    for _ in range(bursts):
        if position in infected:
            direction = (direction + 1) % 4
            infected.remove(position)
        else:
            direction = (direction - 1) % 4
            infected.add(position)
            infections += 1

        row_delta, col_delta = directions[direction]
        position = (position[0] + row_delta, position[1] + col_delta)

    return infections


def evolved_infected_count(text, bursts):
    rows = text.splitlines()
    size = len(rows)
    states = {
        (row, col): "#"
        for row, line in enumerate(rows)
        for col, value in enumerate(line)
        if value == "#"
    }
    position = (size // 2, size // 2)
    direction = 0
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    infections = 0

    for _ in range(bursts):
        state = states.get(position, ".")
        if state == ".":
            direction = (direction - 1) % 4
            states[position] = "W"
        elif state == "W":
            states[position] = "#"
            infections += 1
        elif state == "#":
            direction = (direction + 1) % 4
            states[position] = "F"
        else:
            direction = (direction + 2) % 4
            del states[position]

        row_delta, col_delta = directions[direction]
        position = (position[0] + row_delta, position[1] + col_delta)

    return infections


# test
r_test1 = infected_count(ipt_test, 10000)
print(f"# Test part 1: {r_test1} (expected 5587)")
assert r_test1 == 5587

r1 = infected_count(ipt_puzzle, 10000)
print(f"# Part 1 solution: {r1}")

r_test2 = evolved_infected_count(ipt_test, 100)
print(f"# Test part 2: {r_test2} (expected 26)")
assert r_test2 == 26

r2 = evolved_infected_count(ipt_puzzle, 10000000)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 5450
# Part 2 solution: 2511957
