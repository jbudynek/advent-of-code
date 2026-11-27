# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: depth-first search each bridge starting at port 0, using each
#   component at most once and retaining the strongest total port strength.
# - Part 2: search the same bridges and rank complete candidates primarily by
#   component count, then by total strength for ties.

ipt_test = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

ipt_puzzle = open("input.txt").read().strip()


def parse(text):
    return [tuple(map(int, line.split("/"))) for line in text.splitlines()]


def strongest(text):
    components = parse(text)

    def search(port, unused, strength):
        best = strength
        for index, (left, right) in enumerate(unused):
            if port not in (left, right):
                continue
            remaining = unused[:index] + unused[index + 1:]
            next_port = right if port == left else left
            best = max(best, search(next_port, remaining, strength + left + right))
        return best

    return search(0, components, 0)


# test
r_test1 = strongest(ipt_test)
print(f"# Test part 1: {r_test1} (expected 31)")
assert r_test1 == 31

r1 = strongest(ipt_puzzle)
print(f"# Part 1 solution: {r1}")


def strongest_longest(text):
    components = parse(text)

    def search(port, unused, length, strength):
        best = (length, strength)
        for index, (left, right) in enumerate(unused):
            if port not in (left, right):
                continue
            remaining = unused[:index] + unused[index + 1:]
            next_port = right if port == left else left
            candidate = search(next_port, remaining, length + 1, strength + left + right)
            if candidate > best:
                best = candidate
        return best

    length, strength = search(0, components, 0, 0)
    return strength


r_test2 = strongest_longest(ipt_test)
print(f"# Test part 2: {r_test2} (expected 19)")
assert r_test2 == 19

r2 = strongest_longest(ipt_puzzle)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1868
# Part 2 solution: 1841
