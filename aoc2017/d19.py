# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: follow the grid, turn only at intersections, and collect letters.
# - Part 2: count every entered grid position along the same route, including
#   the starting line and the final letter/end position.

ipt_test = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """

ipt_puzzle = open("input.txt").read().strip("\n")


def route(text):
    grid = text.splitlines()
    width = max(len(row) for row in grid)
    grid = [row.ljust(width) for row in grid]

    y = 0
    x = grid[0].index("|")
    dy, dx = 1, 0
    letters = []
    steps = 0

    while 0 <= y < len(grid) and 0 <= x < width:
        char = grid[y][x]
        if char == " ":
            break

        steps += 1
        if char.isalpha():
            letters.append(char)

        if char == "+":
            choices = []
            for ndy, ndx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (ndy, ndx) == (-dy, -dx):
                    continue
                ny, nx = y + ndy, x + ndx
                if 0 <= ny < len(grid) and 0 <= nx < width and grid[ny][nx] != " ":
                    choices.append((ndy, ndx))
            if not choices:
                break
            dy, dx = choices[0]

        y += dy
        x += dx

    return "".join(letters), steps


# test
r_test1, r_test_steps = route(ipt_test)
print(f"# Test part 1: {r_test1} (expected ABCDEF)")
print(f"# Test part 2: {r_test_steps} (expected 38)")
assert r_test1 == "ABCDEF"
assert r_test_steps == 38

letters, steps = route(ipt_puzzle)
print(f"# Part 1 solution: {letters}")
print(f"# Part 2 solution: {steps}")

# Part 1 solution: PVBSCMEQHY
# Part 2 solution: 17736
