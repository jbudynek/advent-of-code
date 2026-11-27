# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: represent the grid as character rows, generate every rotation and
#   reflection of each input pattern, and apply the matching replacement rules
#   to every 2x2 or 3x3 block for five iterations.
# - Part 2: reuse the same rule matching and block substitution, but continue
#   the 18-iteration enhancement process and count the final lit pixels.

ipt_test = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

ipt_puzzle = open("input.txt").read().strip()


START = ".#.\n..#\n###"


def parse_grid(text):
    return tuple(text.split("/") if "/" in text else text.splitlines())


def grid_text(grid):
    return "/".join(grid)


def rotate(grid):
    size = len(grid)
    return tuple("".join(grid[size - 1 - row][col] for row in range(size)) for col in range(size))


def flip(grid):
    return tuple(row[::-1] for row in grid)


def variants(grid):
    found = set()
    for reflected in (grid, flip(grid)):
        current = reflected
        for _ in range(4):
            found.add(grid_text(current))
            current = rotate(current)
    return found


def parse_rules(text):
    rules = {}
    for line in text.splitlines():
        left, right = line.split(" => ")
        output = parse_grid(right)
        for pattern in variants(parse_grid(left)):
            rules[pattern] = output
    return rules


def enhance(text, iterations, rules_text):
    grid = parse_grid(text)
    rules = parse_rules(rules_text)

    for _ in range(iterations):
        size = len(grid)
        block_size = 2 if size % 2 == 0 else 3
        output_size = block_size + 1
        block_count = size // block_size
        enhanced = [["" for _ in range(output_size * block_count)] for _ in range(output_size * block_count)]

        for block_row in range(block_count):
            for block_col in range(block_count):
                block = tuple(
                    "".join(
                        grid[row][col]
                        for col in range(block_col * block_size, (block_col + 1) * block_size)
                    )
                    for row in range(block_row * block_size, (block_row + 1) * block_size)
                )
                replacement = rules[grid_text(block)]
                for row in range(output_size):
                    for col in range(output_size):
                        enhanced[block_row * output_size + row][block_col * output_size + col] = replacement[row][col]

        grid = tuple("".join(row) for row in enhanced)

    return sum(row.count("#") for row in grid)


# test
r_test1 = enhance(START, 2, ipt_test)
print(f"# Test part 1: {r_test1} (expected 12)")
assert r_test1 == 12

r1 = enhance(START, 5, ipt_puzzle)
print(f"# Part 1 solution: {r1}")

r_test2 = enhance(START, 2, ipt_test)
print(f"# Test part 2: {r_test2} (expected 12)")
assert r_test2 == 12

r2 = enhance(START, 18, ipt_puzzle)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 186
# Part 2 solution: 3018423
