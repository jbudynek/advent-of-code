# coding: utf-8
from timeit import default_timer as timer

# Main function
##########


def step(l):
    ret = ""
    len_l = len(l)
    i = 0
    while i < len_l:
        found = False
        for nn in range(9, 0, -1):
            if not found:
                for nnn in range(9, 0, -1):
                    if not found:
                        lookup = nn * str(nnn)
                        if (i + nn <= len_l) and (l[i : i + nn] == lookup):
                            ret += str(nn) + str(nnn)
                            i = i + nn
                            found = True
    return ret


def boom_part1(input_val, DBG=True):

    l = input_val
    for i in range(40):
        l = step(l)
        if DBG and i < 10:
            print(l)

    return len(l)


def boom_part2(input_val, DBG=True):
    l = input_val
    for i in range(50):
        l = step(l)
        if DBG and i < 10:
            print(l)

    return len(l)


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag == True:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
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


test_part1("1", "82350", True)
test_part2("1", "1166642", True)
# sys.exit()

# Real data
##########

puzzle_input = "1113222113"

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

# PART 1 OK = 252594
# PART 2 OK = 3579328
