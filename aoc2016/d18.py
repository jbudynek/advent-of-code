# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Each new tile is a trap exactly when its left and right parents differ
# (the four trap rules all reduce to left XOR right; the center never matters).
# Treat the row as a string, pad it with safe tiles ('.') on both sides, and
# build each next row by comparing tiles at i-1 and i+1. Count safe tiles
# over the 40 rows.
#
# Part 2: Same simulation, just with 400000 rows; the row-by-row loop keeps
# only the current row in memory, so it simply scales (~400k * width ops).

ipt_test = ".^^.^.^^^^"
ipt_puzzle = open("input.txt").read().strip()


def next_row(row):
    padded = "." + row + "."
    return "".join("^" if padded[i - 1] != padded[i + 1] else "." for i in range(1, len(row) + 1))


def count_safe(row, nb_rows):
    total = 0
    for _ in range(nb_rows):
        total += row.count(".")
        row = next_row(row)
    return total


assert count_safe("..^^.", 3) == 6
assert count_safe(ipt_test, 10) == 38

print("Part 1:", count_safe(ipt_puzzle, 40))
print("Part 2:", count_safe(ipt_puzzle, 400000))

# Part 1 solution: 1987
# Part 2 solution: 19984714
