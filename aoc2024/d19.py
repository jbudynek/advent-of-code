ipt = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".split(
    "\n\n"
)

ipt = open("input-d19.txt").read().split("\n\n")

bricks = ipt[0].strip().split(", ")

lines = ipt[1].split("\n")

CACHE: dict[str, bool] = {}


def is_possible(pattern):
    if pattern in CACHE:
        return CACHE[pattern]

    ret = False
    for brick in bricks:
        if pattern == brick:
            ret = True
            break
        # fmt:off
        elif pattern.startswith(brick) and is_possible(pattern[len(brick):]):
            # fmt:on
            ret = True
            break
    CACHE[pattern] = ret
    return ret


r1 = sum([is_possible(line) for line in lines])

CACHE2: dict[str, int] = {}


def count_possible_ways(pattern):
    if pattern in CACHE2:
        return CACHE2[pattern]

    ret = 0
    for brick in bricks:
        if pattern == brick:
            ret += 1
        elif pattern.startswith(brick):
            # fmt:off
            ret += count_possible_ways(pattern[len(brick):])
            # fmt:on
    CACHE2[pattern] = ret
    return ret


r2 = sum([count_possible_ways(line) for line in lines])

print(r1)
print(r2)
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 319
# Part 2 solution: 692575723305545
