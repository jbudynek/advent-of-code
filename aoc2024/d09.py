# For part 1 you can represent the actual hard drive in memory using an array
# and have two pointers, one to the first free spot, and one to the last spot
# having some file data. You can just switch the values until you're done.
# For part 2, you could also have the whole drive in memory but then it's pretty
# slow to run. Better to represent the data in two parts: one dict that links
# file_id to its position and length, and one that links the start of a free
# spot to its length. Then the algorithm is simple: for each file (decreasing),
# find the leftmost spot that it can fit in, move the file, and update the free
# spot size (or delete it altogether).

ipt = """2333133121414131402"""

ipt = open("input.txt").read().splitlines()[0]

# for part 1
hdd: list[int] = []
ptr_first_free = 10
max_file_id = -1

# for part 2
file_id_to_position_and_len = {}
free_position_to_len = {}

# parse input
cur_pos = 0
for i, n in enumerate(ipt):
    if i % 2 == 0:
        max_file_id += 1
        file_id_to_position_and_len[max_file_id] = (len(hdd), int(n))
        for ff in range(int(n)):
            hdd.append(max_file_id)
        cur_pos += int(n)
    else:
        ptr_first_free = min(cur_pos, ptr_first_free)
        free_position_to_len[cur_pos] = int(n)
        for ff in range(int(n)):
            hdd.append(-1)
        cur_pos += int(n)

# part 1
ptr_last_data = len(hdd) - 1
while True:
    hdd[ptr_first_free], hdd[ptr_last_data] = hdd[ptr_last_data], hdd[ptr_first_free]
    while hdd[ptr_first_free] != -1:
        ptr_first_free += 1
    while hdd[ptr_last_data] == -1:
        ptr_last_data -= 1
    if ptr_first_free == ptr_last_data + 1:
        break

r1 = sum([i * n for i, n in enumerate(hdd) if n != -1])

print(f"# Part 1 solution: {r1}")

# part 2


def find_free_spot(pos_max, len_min):
    for freespot in sorted(free_position_to_len.keys()):
        if free_position_to_len[freespot] >= len_min and freespot < pos_max:
            return freespot
    return -1


for file_id in range(max_file_id, 0, -1):
    pos_file, len_file = file_id_to_position_and_len[file_id]
    pos_free = find_free_spot(pos_file, len_file)

    if pos_free != -1:
        len_free = free_position_to_len[pos_free]
        if len_free == len_file:
            del free_position_to_len[pos_free]
        elif len_free > len_file:
            del free_position_to_len[pos_free]
            free_position_to_len[pos_free + len_file] = len_free - len_file
        file_id_to_position_and_len[file_id] = (pos_free, len_file)

r2 = 0
for file_id in file_id_to_position_and_len.keys():
    pos_file, len_file = file_id_to_position_and_len[file_id]
    r2 += file_id * (pos_file * len_file + (sum(range(len_file))))

print(f"# Part 2 solution: {r2}")

# Part 1 solution: 6519155389266
# Part 2 solution: 6547228115826
