# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model)
# Simulate every acre's simultaneous transition from the starting adjacent-acre counts.
# For part 2, detect a repeated landscape and skip complete cycles before computing the resource value.

ipt_test = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

ipt_puzzle = open("input.txt").read().strip()


def step(grid):
    height = len(grid)
    width = len(grid[0])
    new_grid = []
    for row in range(height):
        new_row = []
        for col in range(width):
            neighbors = [
                grid[nr][nc]
                for nr in range(max(0, row - 1), min(height, row + 2))
                for nc in range(max(0, col - 1), min(width, col + 2))
                if (nr, nc) != (row, col)
            ]
            current = grid[row][col]
            if current == "." and neighbors.count("|") >= 3:
                new_row.append("|")
            elif current == "|" and neighbors.count("#") >= 3:
                new_row.append("#")
            elif current == "#" and "#" in neighbors and "|" in neighbors:
                new_row.append("#")
            elif current == "#":
                new_row.append(".")
            else:
                new_row.append(current)
        new_grid.append(new_row)
    return new_grid


def resource_value(grid):
    wooded = sum(row.count("|") for row in grid)
    lumberyards = sum(row.count("#") for row in grid)
    return wooded * lumberyards


def simulate(initial, minutes):
    grid = [list(row) for row in initial.strip().splitlines()]
    seen = {}

    minute = 0
    while minute < minutes:
        state = tuple("".join(row) for row in grid)
        if state in seen:
            cycle = minute - seen[state]
            remaining = (minutes - minute) // cycle
            if remaining:
                minute += remaining * cycle
                continue
        else:
            seen[state] = minute

        grid = step(grid)
        minute += 1

    return resource_value(grid)


assert simulate(ipt_test, 10) == 1147

print("Part 1:", simulate(ipt_puzzle, 10))
print("Part 2:", simulate(ipt_puzzle, 1_000_000_000))

# Part 1 solution: 506160
# Part 2 solution: 189168
