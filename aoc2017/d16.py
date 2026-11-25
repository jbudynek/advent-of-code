# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# The dance is a list of moves applied to a line of programs (a string/list).
# - Spin sX: rotate the line so the last X programs come first.
# - Exchange xA/B: swap the programs at positions A and B.
# - Partner pA/B: find the positions of programs A and B and swap them.
# - Part 1: apply every move once, in order, and read the final line.
# - Part 2: repeat the whole dance 1e9 times. The sequence of lines is periodic
#   (the dance is a permutation, so it must return to the start), so simulate
#   dances until the starting line reappears, find the period P, then only
#   1e9 % P dances are needed.

ipt_test = "s1,x3/4,pe/b"

ipt_puzzle = open("input.txt").read().strip()


def dance(moves, line):
    line = list(line)
    for m in moves.split(","):
        if m[0] == "s":
            x = int(m[1:])
            line = line[-x:] + line[:-x]
        elif m[0] == "x":
            a, b = map(int, m[1:].split("/"))
            line[a], line[b] = line[b], line[a]
        else:
            a, b = m[1:].split("/")
            i, j = line.index(a), line.index(b)
            line[i], line[j] = line[j], line[i]
    return "".join(line)


def dance_many(moves, line, n=1_000_000_000):
    start = line
    period = 0
    cur = line
    while True:
        cur = dance(moves, cur)
        period += 1
        if cur == start:
            break
    cur = line
    for _ in range(n % period):
        cur = dance(moves, cur)
    return cur


# test
r_test1 = dance(ipt_test, "abcde")
print(f"# Test part 1: {r_test1} (expected baedc)")
assert r_test1 == "baedc"

# test part 2: with 5 programs, 2 dances give ceadb
assert dance(ipt_test, dance(ipt_test, "abcde")) == "ceadb"
assert dance_many(ipt_test, "abcde", 2) == "ceadb"

r1 = dance(ipt_puzzle, "abcdefghijklmnop")
print(f"# Part 1 solution: {r1}")
r2 = dance_many(ipt_puzzle, "abcdefghijklmnop")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: padheomkgjfnblic
# Part 2 solution: bfcdeakhijmlgopn
