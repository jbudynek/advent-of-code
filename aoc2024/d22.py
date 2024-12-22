import re

ipt_1_37327623 = """1
10
100
2024"""

ipt_2_23 = """1
2
3
2024"""

ipt = ipt_2_23

ipt = open("input-d22.txt").read()

buyers_secret = list(map(int, re.findall(r"-?\d+", ipt)))

max_rounds = 2000

# part 1


def mix(number, value):
    return number ^ value


def prune(number):
    return number % 16777216


ret1 = []

for secnum in buyers_secret:
    for r in range(max_rounds):
        # 1
        secnum_m64 = secnum * 64
        secnum = mix(secnum, secnum_m64)
        secnum = prune(secnum)
        # 2
        secnum_d32 = secnum // 32
        secnum = mix(secnum, secnum_d32)
        secnum = prune(secnum)
        # 3
        secnum_m2048 = secnum * 2048
        secnum = mix(secnum, secnum_m2048)
        secnum = prune(secnum)
    ret1.append(secnum)

r1 = sum(ret1)
print(f"# Part 1 solution: {r1}")

# part 2 - I dont' know why we need 1 more round, but so it is!
all_sequences = set()
buyer_to_prices: dict[int, list[int]] = {}
buyer_to_deltas: dict[int, list[int]] = {}
buyer_to_r_of_first_seq: dict[int, dict[tuple, int]] = {}

for idx_buyer, secnum in enumerate(buyers_secret):
    if idx_buyer % 500 == 0:
        print(idx_buyer, len(buyers_secret))
    buyer_to_prices[idx_buyer] = []
    buyer_to_deltas[idx_buyer] = []
    buyer_to_r_of_first_seq[idx_buyer] = {}
    for r in range(max_rounds + 1):
        # 1
        secnum_m64 = secnum * 64
        secnum = mix(secnum, secnum_m64)
        secnum = prune(secnum)
        # 2
        secnum_d32 = secnum // 32
        secnum = mix(secnum, secnum_d32)
        secnum = prune(secnum)
        # 3
        secnum_m2048 = secnum * 2048
        secnum = mix(secnum, secnum_m2048)
        secnum = prune(secnum)

        buyer_to_prices[idx_buyer].append(secnum % 10)
        if r == 0:
            buyer_to_deltas[idx_buyer].append(0)
        else:
            buyer_to_deltas[idx_buyer].append(
                buyer_to_prices[idx_buyer][r] - buyer_to_prices[idx_buyer][r - 1]
            )

        if r <= 3:
            pass
        else:
            seq = tuple([buyer_to_deltas[idx_buyer][r - 3 + i] for i in range(4)])
            all_sequences.add(seq)
            if seq not in buyer_to_r_of_first_seq[idx_buyer]:
                buyer_to_r_of_first_seq[idx_buyer][seq] = r


seq2bananas = {}
for nseq, seq in enumerate(all_sequences):
    if nseq % 500 == 0:
        print(nseq, len(all_sequences))
    seq2bananas[seq] = 0
    for idx_buyer, secnum in enumerate(buyers_secret):
        if seq in buyer_to_r_of_first_seq[idx_buyer]:
            r = buyer_to_r_of_first_seq[idx_buyer][seq]
            seq2bananas[seq] += buyer_to_prices[idx_buyer][r]

max_bananas = 0
for k, v in seq2bananas.items():
    if v > max_bananas:
        max_bananas = v
        print(k, v)


r2 = max_bananas

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 19854248602
# Part 2 solution: 2223
