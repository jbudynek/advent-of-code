# Algorithm (code written by Claude, an AI assistant made by Anthropic)
#
# Part 1: Generate the MD5 stream lazily with a cache (each index is hashed
# only once, since every candidate looks 1000 hashes ahead). For each index,
# find the first triplet character in its hash with a regex; if there is one,
# the index is a key when any of the next 1000 hashes contains that character
# five times in a row. Count keys until the 64th and return its index.
#
# Part 2: Same search, but each hash is "stretched": after the first MD5, the
# hex digest is re-hashed 2016 more times (2017 MD5 calls in total). This is a
# `stretch` parameter of the hash function; the cache matters even more here.

import hashlib
import re
from timeit import default_timer as timer


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


def find_key(salt, nth=64, stretch=0):
    cache = {}

    def h(i):
        if i not in cache:
            d = hashlib.md5((salt + str(i)).encode()).hexdigest()
            for _ in range(stretch):
                d = hashlib.md5(d.encode()).hexdigest()
            cache[i] = d
        return cache[i]

    found = 0
    i = 0
    while True:
        m = re.search(r"(.)\1\1", h(i))
        if m:
            five = m.group(1) * 5
            if any(five in h(j) for j in range(i + 1, i + 1001)):
                found += 1
                if found == nth:
                    return i
        i += 1


ipt_test = "abc"
ipt_puzzle = open("input.txt").read().strip()

assert find_key(ipt_test) == 22728
assert find_key(ipt_test, stretch=2016) == 22551

print("Part 1:", find_key(ipt_puzzle))
t_start = timer()
result = find_key(ipt_puzzle, stretch=2016)
t_end = timer()
print_time(t_start, t_end)
print("Part 2:", result)

# Part 1 solution: 15035
# Part 2 solution: 19968
# Part 2 duration: ~20 s (20242 ms)
