ipt_test = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

ipt_puzzle = open("input.txt").read()

ipt = ipt_puzzle

sout_1 = set()
sout_2 = set()
for r in ipt.split(","):
    start_s, end_s = r.split("-")
    hs = 0
    if len(start_s) == 1:
        hs = 0
    else:
        hs = int(start_s[0 : len(start_s) // 2])

    start = int(start_s)
    end = int(end_s)

    for j in range(2, len(end_s) + 1):
        hs = 0
        if len(start_s) // j == 0:
            hs = 0
        else:
            hs = int(start_s[0 : len(start_s) // j])
        for i in range(hs, end + 1):
            test = int(j * str(i))
            if test >= start and test <= end:
                if j == 2:
                    sout_1.add(test)
                sout_2.add(test)
            if test > end:
                break

print(f"# Part 1 solution: {sum(list(sout_1))}")
print(f"# Part 2 solution: {sum(list(sout_2))}")

# Part 1 solution: 23701357374
# Part 2 solution: 34284458938
