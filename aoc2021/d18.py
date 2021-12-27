# coding: utf-8
import copy
from timeit import default_timer as timer

import numpy as np

# Main function
##########


class Pair:
    def __init__(self, lhs, rhs, parent):
        self.lhs = lhs
        self.rhs = rhs
        self.parent = parent

    def __str__(self):
        return "["+str(self.lhs)+","+str(self.rhs)+"]"


class RegularNumber:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def __str__(self):
        return str(self.value)


def increase_depth(n, d_map):
    if isinstance(n, RegularNumber):
        return None
    else:
        if d_map[n] == 4:
            return n
        d_map[n.lhs] = d_map[n] + 1
        d_map[n.rhs] = d_map[n] + 1
        ret = increase_depth(n.lhs, d_map)
        if ret != None:
            return ret
        ret = increase_depth(n.rhs, d_map)
        if ret != None:
            return ret


def find_deep_pair(root):
    d_map = {}
    d_map[root] = 0

    pair = increase_depth(root, d_map)
    return pair


def look_for_ten(n, n_map):
    if isinstance(n, RegularNumber) and n.value >= 10:
        return n
    elif isinstance(n, RegularNumber):
        return None
    else:
        ret = look_for_ten(n.lhs, n_map)
        if ret != None:
            return ret
        ret = look_for_ten(n.rhs, n_map)
        if ret != None:
            return ret


def find_big_number(root):
    n_map = {}
    n_map[root] = 0

    pair = look_for_ten(root, n_map)
    return pair


def reduce(pair, DBG=True):

    cont = True

    while cont:
        while cont:
            cont = False
            # If any pair is nested inside four pairs, the leftmost such pair explodes.

            l_to_r = build_left_to_right(pair)

            # find first pair that has depth >=4
            to_explode = find_deep_pair(pair)
            # explode
            if to_explode != None:
                explode(to_explode, l_to_r)
                cont = True

        cont = False

        # If any regular number is 10 or greater, the leftmost such regular number splits

        # find first reg num >= 10
        bigger_than_ten = find_big_number(pair)
        # split
        if bigger_than_ten != None:
            split(bigger_than_ten)
            cont = True


def explore(n, l_to_r):
    if isinstance(n, RegularNumber):
        l_to_r.append(n)
    else:
        explore(n.lhs, l_to_r)
        explore(n.rhs, l_to_r)


def build_left_to_right(root):

    l_to_r = []
    explore(root, l_to_r)

    return l_to_r


def fing_reg_num_to_the_left(regnum, l_to_r):
    l = len(l_to_r)
    for i in range(l):
        if l_to_r[i] == regnum and i > 0:
            return l_to_r[i-1]
    return None


def fing_reg_num_to_the_right(regnum, l_to_r):
    l = len(l_to_r)
    for i in range(l):
        if l_to_r[i] == regnum and i < l-1:
            return l_to_r[i+1]
    return None


def explode(pair, l_to_r):
    # To explode a pair, the pair's left value is added to the first regular number
    # to the left of the exploding pair (if any), and the pair's right value is added
    # to the first regular number to the right of the exploding pair (if any). Exploding pairs
    # will always consist of two regular numbers. Then, the entire exploding pair is replaced
    # with the regular number 0.

    regnum_left = fing_reg_num_to_the_left(pair.lhs, l_to_r)
    regnum_right = fing_reg_num_to_the_right(pair.rhs, l_to_r)
    if regnum_left != None:
        regnum_left.value += pair.lhs.value
    if regnum_right != None:
        regnum_right.value += pair.rhs.value

    if pair.parent.lhs == pair:
        pair.parent.lhs = RegularNumber(0, pair.parent)
    else:
        pair.parent.rhs = RegularNumber(0, pair.parent)


def split(regnum):
    # To split a regular number, replace it with a pair; the left element of the pair
    # should be the regular number divided by two and rounded down, while the right
    # element of the pair should be the regular number divided by two and rounded up.
    # For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    newpair = Pair(None, None, None)
    newpair.lhs = RegularNumber(regnum.value//2, newpair)
    newpair.rhs = RegularNumber(
        (regnum.value//2) + (regnum.value % 2), newpair)

    if regnum.parent.lhs == regnum:
        regnum.parent.lhs = newpair
        newpair.parent = regnum.parent
    else:
        regnum.parent.rhs = newpair
        newpair.parent = regnum.parent


def sf_add(lhsf, rhsf, DBG=True):
    ret = Pair(lhsf, rhsf, None)
    lhsf.parent = ret
    rhsf.parent = ret
    reduce(ret, DBG)
    return ret


def parse_sf(lll, DBG=True):
    idx = 0
    l = len(lll)

    root = Pair(None, None, None)
    idx += 1
    cur = root
    while idx < l:
        c = lll[idx]
        if c == '[':
            node = Pair(None, None, cur)
            if cur.lhs == None:
                cur.lhs = node
            else:
                cur.rhs = node
            cur = node
        elif c == ',':
            cur = cur.parent
        elif c == ']':
            cur = cur.parent
        else:
            num = RegularNumber(int(c), cur)
            if cur.lhs == None:
                cur.lhs = num
            else:
                cur.rhs = num
            cur = num
        idx += 1

    if DBG:
        print(str(root))

    return root


def magnitude(n):
    if isinstance(n, RegularNumber):
        return n.value
    else:
        return 3*magnitude(n.lhs)+2*magnitude(n.rhs)


def boom_part1(input_val, DBG=True):

    sum_sf = parse_sf(input_val[0])

    for lll in input_val[1:]:
        to_add = parse_sf(lll, DBG)

        new_sum_sf = sf_add(sum_sf, to_add, DBG)

        if DBG:
            print("= ", str(new_sum_sf))

        sum_sf = new_sum_sf

    return str(sum_sf)


def boom_part2(input_val, DBG=True):
    all_fishes = []
    sum_sf = parse_sf(input_val[0], DBG)

    for lll in input_val:
        all_fishes.append(parse_sf(lll, DBG))

    l = len(all_fishes)
    max_val = 0

    for i in range(l):
        for j in range(l):
            if i != j:
                max_val = max(max_val, magnitude(
                    sf_add(copy.deepcopy(all_fishes[i]), copy.deepcopy(all_fishes[j]))))

    return max_val

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


# tests explode
root = parse_sf('[[[[[9,8],1],2],3],4]')
l_to_r = build_left_to_right(root)
to_explode = find_deep_pair(root)
explode(to_explode, l_to_r)
print(str(root))  # [[[[0,9],2],3],4]

root = parse_sf('[7,[6,[5,[4,[3,2]]]]]')
l_to_r = build_left_to_right(root)
to_explode = find_deep_pair(root)
explode(to_explode, l_to_r)
print(str(root))  # [7,[6,[5,[7,0]]]]

root = parse_sf('[[6,[5,[4,[3,2]]]],1]')
l_to_r = build_left_to_right(root)
to_explode = find_deep_pair(root)
explode(to_explode, l_to_r)
print(str(root))  # [[6,[5,[7,0]]],3]

root = parse_sf('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
l_to_r = build_left_to_right(root)
to_explode = find_deep_pair(root)
explode(to_explode, l_to_r)
print(str(root))  # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]

root = parse_sf('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
l_to_r = build_left_to_right(root)
to_explode = find_deep_pair(root)
explode(to_explode, l_to_r)
print(str(root))  # [[3,[2,[8,0]]],[9,[5,[7,0]]]]

# tests sums
tt1 = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"""
tt1 = tt1.splitlines()
test_part1(tt1, "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", True)

tt1 = """[1,1]
[2,2]
[3,3]
[4,4]"""
tt1 = tt1.splitlines()
test_part1(tt1, "[[[[1,1],[2,2]],[3,3]],[4,4]]", True)

tt1 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
tt1 = tt1.splitlines()
test_part1(tt1, "[[[[3,0],[5,3]],[4,4]],[5,5]]", True)

tt1 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
tt1 = tt1.splitlines()
test_part1(tt1, "[[[[5,0],[7,4]],[5,5]],[6,6]]", True)


tt1 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
tt1 = tt1.splitlines()
test_part1(tt1, "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", True)

# Test magnitudes
mag = magnitude(parse_sf("[[1,2],[[3,4],5]]"))
print(mag, mag == 143)
mag = magnitude(parse_sf("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))
print(mag, mag == 1384)
mag = magnitude(parse_sf("[[[[1,1],[2,2]],[3,3]],[4,4]]"))
print(mag, mag == 445)
mag = magnitude(parse_sf("[[[[3,0],[5,3]],[4,4]],[5,5]]"))
print(mag, mag == 791)
mag = magnitude(parse_sf("[[[[5,0],[7,4]],[5,5]],[6,6]]"))
print(mag, mag == 1137)
mag = magnitude(
    parse_sf("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))
print(mag, mag == 3488)


tt1 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
tt1 = tt1.splitlines()
test_part1(
    tt1, "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]", True)
mag = magnitude(
    parse_sf("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"))
print(mag, mag == 4140)

# test part 2

tt1 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
tt1 = tt1.splitlines()
test_part2(tt1, 3993, True)

# Real data
##########

INPUT_FILE = "input-d18.txt"
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
print(magnitude(parse_sf(ret)))

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 4137
# PART 2 OK = 4573
