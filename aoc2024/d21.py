from collections import Counter

import numpy as np

ipt_1_126384 = """029A
980A
179A
456A
379A""".split(
    "\n"
)

ipt = ipt_1_126384

ipt = open("input-d21.txt").read().strip().split("\n")


digicode = {
    "7": 0 + 0j,
    "8": 1 + 0j,
    "9": 2 + 0j,
    "4": 0 + 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "1": 0 + 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    "0": 1 + 3j,
    "A": 2 + 3j,
}

diricode = {
    "^": 1 + 0j,
    "A": 2 + 0j,
    "<": 0 + 1j,
    "v": 1 + 1j,
    ">": 2 + 1j,
}

seed = 3141592  # Knuth's Pi

np.random.seed(seed)

CACHE_PATH: dict[tuple, str] = {}


def compute_path(from_, to_, key_to_pos):

    if (from_, to_) in CACHE_PATH:
        return CACHE_PATH[(from_, to_)]

    ret = ""

    dz = key_to_pos[to_] - key_to_pos[from_]
    dz_r = int(dz.real)
    dz_i = int(dz.imag)

    cur0 = key_to_pos[from_]
    ret0 = ret
    cur = cur0

    coin = np.random.choice([0, 1])

    if coin == 0:
        try:
            # UD then LR
            ret = ret0
            cur = cur0

            cur += 1j * dz_i
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_i < 0:
                ret += -dz_i * "^"
            else:
                ret += dz_i * "v"

            cur += dz_r
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_r < 0:
                ret += -dz_r * "<"
            else:
                ret += dz_r * ">"
            # end UD then LR

        except Exception:
            # LR then UD
            ret = ret0
            cur = cur0

            cur += dz_r
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_r < 0:
                ret += -dz_r * "<"
            else:
                ret += dz_r * ">"

            cur += 1j * dz_i
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_i < 0:
                ret += -dz_i * "^"
            else:
                ret += dz_i * "v"
            # end LR then UD

    elif coin == 1:
        try:
            # LR then UD
            ret = ret0
            cur = cur0

            cur += dz_r
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_r < 0:
                ret += -dz_r * "<"
            else:
                ret += dz_r * ">"

            cur += 1j * dz_i
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_i < 0:
                ret += -dz_i * "^"
            else:
                ret += dz_i * "v"
            # end LR then UD

        except Exception:
            # UD then LR
            ret = ret0
            cur = cur0

            cur += 1j * dz_i
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_i < 0:
                ret += -dz_i * "^"
            else:
                ret += dz_i * "v"

            cur += dz_r
            if cur not in key_to_pos.values():
                raise (Exception("should not be here"))

            if dz_r < 0:
                ret += -dz_r * "<"
            else:
                ret += dz_r * ">"
            # end UD then LR

    ret += "A"

    CACHE_PATH[(from_, to_)] = ret
    return ret


CACHE_LEN: dict[str, int] = {}


def compute_length(code, depth, max_depth):
    if (code, depth) in CACHE_LEN:
        return CACHE_LEN[(code, depth)]
    if depth == 0:
        return len(code)  # digicode
    length = 0
    key_to_pos = diricode
    if depth == max_depth:
        key_to_pos = digicode
    for idx, digit in enumerate(code):
        if idx == 0:
            length += compute_length(
                compute_path("A", digit, key_to_pos), depth - 1, max_depth
            )
        else:
            length += compute_length(
                compute_path(code[idx - 1], digit, key_to_pos), depth - 1, max_depth
            )
    CACHE_LEN[(code, depth)] = length
    return length


# Part 1
all_r1s = []

for i in range(1000):
    CACHE_LEN = {}
    CACHE_PATH = {}
    if i % 100 == 0:
        print(i)
    r1 = 0
    for code in ipt:
        # once with digicode, twice with diricode
        length = compute_length(code, 3, 3)
        num = int(code[0:-1])
        r1 += length * num
    all_r1s.append(r1)

c1 = Counter(all_r1s)
sorted_counter1 = dict(sorted(c1.items()))
r1 = list(sorted_counter1.keys())[0]
print("**", r1)

# P2
all_r2s = []

for i in range(1000):
    CACHE_LEN = {}
    CACHE_PATH = {}
    if i % 100 == 0:
        print(i)
    r2 = 0
    for code in ipt:
        # once with digicode, 25 times with diricode
        length = compute_length(code, 26, 26)
        num = int(code[0:-1])
        r2 += length * num
    all_r2s.append(r2)

c2 = Counter(all_r2s)
sorted_counter2 = dict(sorted(c2.items()))
r2 = list(sorted_counter2.keys())[0]
print("**", r2)

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 242484
# Part 2 solution: 294209504640384
