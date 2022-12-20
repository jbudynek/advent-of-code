# coding: utf-8
import copy
import sys

from boilerplate import read_input_file, run_func, test_func

# Main function
##########


def mix(input_val, nb_times, decryption_key, DBG):

    # store index and value, because there are duplicates!

    in_idx_val_list = list(enumerate(int(ss) * decryption_key for ss in input_val))

    nb_inputs = len(in_idx_val_list)

    out_idx_val_list = copy.deepcopy(in_idx_val_list)

    for _ in range(nb_times):
        for in_idx in range(nb_inputs):
            in_idx_val = in_idx_val_list[in_idx]
            out_idx_val = out_idx_val_list.index(in_idx_val)

            out_idx_val_list.remove(in_idx_val)

            # modulo nb_inputs-1 !!
            new_jdx = (out_idx_val + in_idx_val[1]) % (nb_inputs - 1)

            out_idx_val_list.insert(new_jdx, in_idx_val)

            if DBG:
                print(out_idx_val_list)

    # find the zero in the output
    idx0 = -1
    for out_idx, out_idx_val in enumerate(out_idx_val_list):
        if out_idx_val[1] == 0:
            idx0 = out_idx

    v1000 = out_idx_val_list[(idx0 + 1000) % nb_inputs][1]
    v2000 = out_idx_val_list[(idx0 + 2000) % nb_inputs][1]
    v3000 = out_idx_val_list[(idx0 + 3000) % nb_inputs][1]

    return v1000 + v2000 + v3000


def boom_part1(input_val, DBG=True):

    return mix(input_val, 1, 1, DBG)


def boom_part2(input_val, DBG=True):

    return mix(input_val, 10, 811589153, DBG)


# Test cases
##########


t1 = """1
2
-3
3
-2
0
4"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 3, True)
test_func(boom_part2, tt1, 1623178306, True)

# Real data
##########

puzzle_input = read_input_file("input-d20.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 2827
# PART 2 OK = 7834270093909

sys.exit()
