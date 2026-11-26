# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Grow the data with the modified dragon curve (a + "0" + reversed,
# inverted a) until it is at least as long as the disk, truncate to the disk
# length, then repeatedly collapse pairs (equal -> "1", different -> "0")
# until the checksum has odd length.
#
# Part 2: Same procedure on a 35.6M-character disk. Pair-collapsing is slow
# on that size, so use a shortcut: repeating the collapse until odd length is
# equivalent to cutting the data into blocks of 2^k characters (2^k = largest
# power of two dividing the length) and emitting "1" for a block with an even
# number of 1s, "0" otherwise.
ipt_test = "10000"
ipt_puzzle = open("input.txt").read().strip()


def dragon(a, size):
    while len(a) < size:
        b = a[::-1].translate(str.maketrans("01", "10"))
        a = a + "0" + b
    return a[:size]


def checksum(data):
    block = len(data) & -len(data)
    return "".join(
        "1" if data.count("1", i, i + block) % 2 == 0 else "0"
        for i in range(0, len(data), block)
    )


def solve(ipt, size):
    return checksum(dragon(ipt, size))


assert dragon("1", 3) == "100"
assert dragon("111100001010", 25) == "1111000010100101011110000"
assert solve(ipt_test, 20) == "01100"
print("Part 1:", solve(ipt_puzzle, 272))
print("Part 2:", solve(ipt_puzzle, 35651584))

# Part 1 solution: 00000100100001100
# Part 2 solution: 00011010100010010
