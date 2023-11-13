# coding: utf-8
from timeit import default_timer as timer

# Main function
##########


def check_line(ll):
    scores_check = {")": 3, "]": 57, "}": 1197, ">": 25137}
    opens = ["(", "[", "{", "<"]
    open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
    current_opens = []
    for cc in ll:
        if cc in opens:
            current_opens.append(cc)
        else:
            if cc != open_to_close[current_opens[len(current_opens) - 1]]:
                return scores_check[cc]
            else:
                del current_opens[len(current_opens) - 1]
    return 0


def boom_part1(input_val, DBG=True):
    return sum(check_line(ll) for ll in input_val)


def complete_line(ll):
    scores_complete = {")": 1, "]": 2, "}": 3, ">": 4}
    opens = ["(", "[", "{", "<"]
    open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
    current_opens = []
    for cc in ll:
        if cc in opens:
            current_opens.append(cc)
        else:
            del current_opens[len(current_opens) - 1]
    ret = 0
    for k in reversed(current_opens):
        ret *= 5
        ret += scores_complete[open_to_close[k]]
    return ret


def boom_part2(input_val, DBG=True):
    ret = []
    for ll in input_val:
        if check_line(ll) != 0:
            continue
        ret.append(complete_line(ll))
    return sorted(ret)[len(ret) // 2]


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
    if flag:
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


tt1 = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 26397, True)
test_part2(tt1, 288957, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d10.txt"
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

# PART 1 OK = 268845
# PART 2 OK = 4038824534
