ipt = """125 17"""
ipt = open("input.txt").read()

stones = [int(e) for e in ipt.split()]

CACHE: dict[tuple, int] = {}


def count(val, rounds_left):
    if rounds_left == 0:
        return 1
    elif (val, rounds_left) in CACHE:
        return CACHE[(val, rounds_left)]
    else:
        if val == 0:
            CACHE[(val, rounds_left)] = count(1, rounds_left - 1)
            return CACHE[(val, rounds_left)]
        elif len(str(val)) % 2 == 0:
            n = str(val)
            # fmt:off
            n1 = int(n[:len(n) // 2])
            n2 = int(n[len(n) // 2:])
            # fmt:on
            CACHE[(val, rounds_left)] = count(n1, rounds_left - 1) + count(
                n2, rounds_left - 1
            )
            return CACHE[(val, rounds_left)]
        else:
            CACHE[(val, rounds_left)] = count(val * 2024, rounds_left - 1)
            return CACHE[(val, rounds_left)]


r1 = sum([count(stone, 25) for stone in stones])
r2 = sum([count(stone, 75) for stone in stones])

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 220999
# Part 2 solution: 261936432123724
