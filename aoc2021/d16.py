# coding: utf-8
from timeit import default_timer as timer

import numpy as np

# Main function
##########


class Node:
    pass


def decode_bin(bline, cursor):
    n = Node()
    n.version = int(bline[cursor+0:cursor+3], 2)
    n.type_id = int(bline[cursor+3:cursor+6], 2)
    n.sub_nodes = []
    if n.type_id == 4:
        cursor += 6
        bnum = ''
        while True:
            chunk = bline[cursor:cursor+5]
            bnum += chunk[1:5]
            cursor += 5
            if chunk[0] == '1':
                continue
            else:
                break
        n.literal_value = int(bnum, 2)
        return (n, bline, cursor)
    else:
        length_type_id = bline[cursor+6]
        if length_type_id == '0':
            total_length_in_bits = int(bline[cursor+7:cursor+7+15], 2)
            c0 = cursor+7+15
            cursor = c0
            while cursor < c0+total_length_in_bits:
                (sn, bline, cursor) = decode_bin(bline, cursor)
                n.sub_nodes.append(sn)
        else:
            number_of_sub_packets_immediately_contained = int(
                bline[cursor+7:cursor+7+11], 2)
            nb = 0
            cursor = cursor+7+11
            while nb < number_of_sub_packets_immediately_contained:
                (sn, bline, cursor) = decode_bin(bline, cursor)
                n.sub_nodes.append(sn)
                nb += 1
    return (n, bline, cursor)


def sum_versions_sub_nodes(n):
    ret = 0
    for sn in n.sub_nodes:
        ret += sum_versions_sub_nodes(sn) + sn.version
    return ret


def operate(n):
    if n.type_id == 4:
        return n.literal_value
    else:
        ret = []
        for sn in n.sub_nodes:
            ret.append(operate(sn))
        if n.type_id == 0:  # sum
            return sum(ret)
        elif n.type_id == 1:  # prod
            return np.product(ret)
        elif n.type_id == 2:  # min
            return min(ret)
        elif n.type_id == 3:  # max
            return max(ret)
        elif n.type_id == 5:  # greater than
            if ret[0] > ret[1]:
                return 1
            else:
                return 0
        elif n.type_id == 6:  # less than
            if ret[0] < ret[1]:
                return 1
            else:
                return 0
        elif n.type_id == 7:  # equal
            if ret[0] == ret[1]:
                return 1
            else:
                return 0


def decode_hex_operate(line):
    nb_bits = len(line)*4
    bline = format(int(line, 16), "0"+str(nb_bits)+"b")
    (n, bline, cursor) = decode_bin(bline, 0)

    ret = operate(n)

    return ret


def decode_hex_sum_version(line):
    nb_bits = len(line)*4
    bline = format(int(line, 16), "0"+str(nb_bits)+"b")
    (n, bline, cursor) = decode_bin(bline, 0)

    ret = 0
    ret += sum_versions_sub_nodes(n) + n.version

    return ret


def boom_part1(input_val, DBG=True):

    ret = 0
    for line in input_val:
        val = decode_hex_sum_version(line)
        ret += val

    return ret


def boom_part2(input_val, DBG=True):
    ret = 0
    for line in input_val:
        val = decode_hex_operate(line)
        ret += val

    return ret

# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)

# Test cases
##########


tt1 = "D2FE28"
tt1 = tt1.splitlines()
test_part1(tt1, 6, True)

tt1 = "38006F45291200"
tt1 = tt1.splitlines()
test_part1(tt1, 9, True)

tt1 = "EE00D40C823060"
tt1 = tt1.splitlines()
test_part1(tt1, 14, True)

tt1 = "8A004A801A8002F478"
tt1 = tt1.splitlines()
test_part1(tt1, 16, True)

tt1 = "620080001611562C8802118E34"
tt1 = tt1.splitlines()
test_part1(tt1, 12, True)

tt1 = "C0015000016115A2E0802F182340"
tt1 = tt1.splitlines()
test_part1(tt1, 23, True)

tt1 = "A0016C880162017C3686B18A3D4780"
tt1 = tt1.splitlines()
test_part1(tt1, 31, True)

tt1 = "C200B40A82"
tt1 = tt1.splitlines()
test_part2(tt1, 3, True)

tt1 = "04005AC33890"
tt1 = tt1.splitlines()
test_part2(tt1, 54, True)

tt1 = "880086C3E88112"
tt1 = tt1.splitlines()
test_part2(tt1, 7, True)

tt1 = "CE00C43D881120"
tt1 = tt1.splitlines()
test_part2(tt1, 9, True)

tt1 = "D8005AC2A8F0"
tt1 = tt1.splitlines()
test_part2(tt1, 1, True)

tt1 = "F600BC2D8F"
tt1 = tt1.splitlines()
test_part2(tt1, 0, True)

tt1 = "9C005AC2F8F0"
tt1 = tt1.splitlines()
test_part2(tt1, 0, True)

tt1 = "9C0141080250320F1802104A08"
tt1 = tt1.splitlines()
test_part2(tt1, 1, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d16.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 908
# PART 2 OK = 10626195124371
