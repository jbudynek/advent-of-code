# coding: utf-8
from timeit import default_timer as timer

# Main function
##########


def parse_line(ll, DBG=True):
    l_r = ll.split(" | ")
    signal_patterns = l_r[0].split()
    output_digits = l_r[1].split()
    return (signal_patterns, output_digits)


def boom_part1(input_val, DBG=True):
    ret = 0
    for ll in input_val:
        (signal_patterns, output_digits) = parse_line(ll, DBG)
        for d in output_digits:
            if (len(d)) in [2, 3, 4, 7]:
                ret += 1
    return ret


def compute_value(signal_patterns, output_digits, DBG):
    letters_to_int = {"abcefg": 0, "cf": 1, "acdeg": 2, "acdfg": 3,
                      "bcdf": 4, "abdfg": 5, "abdefg": 6, "acf": 7, "abcdefg": 8, "abcdfg": 9}
    segment_to_letter = {}
    len_to_pattern = {}

    # index = length - value = list of corresponding patterns
    for i in range(len(signal_patterns)):
        signal_patterns[i] = ''.join(signal_patterns[i])
        if len(signal_patterns[i]) not in len_to_pattern:
            len_to_pattern[len(signal_patterns[i])] = []
        len_to_pattern[len(signal_patterns[i])].append(set(signal_patterns[i]))

    # use 1 and 7 to find a
    segment_to_letter["a"] = len_to_pattern[2][0] ^ len_to_pattern[3][0]

    # collapse all numbers with 6 segments, and use 7, to find c
    all_6 = (len_to_pattern[6][0] & len_to_pattern[6]
             [1] & len_to_pattern[6][2])
    segment_to_letter["c"] = len_to_pattern[3][0] - all_6

    # collapse all numbers with 5 segments, and use 4, to find d
    all_5 = (len_to_pattern[5][0] & len_to_pattern[5]
             [1] & len_to_pattern[5][2])
    segment_to_letter["d"] = all_5 & len_to_pattern[4][0]

    # now it's easy, use 7 and remove segments to find f
    segment_to_letter["f"] = len_to_pattern[3][0] - \
        segment_to_letter["a"] - segment_to_letter["c"]

    # use 4 and remove segments to find b
    segment_to_letter["b"] = len_to_pattern[4][0] - \
        segment_to_letter["c"] - \
        segment_to_letter["d"] - segment_to_letter["f"]

    # use collapsed 5 segments and remove more segments to find g
    segment_to_letter["g"] = all_5 - \
        segment_to_letter["a"] - segment_to_letter["d"]

    # e is the last one
    segment_to_letter["e"] = len_to_pattern[7][0] - segment_to_letter["a"] - segment_to_letter["b"] - \
        segment_to_letter["c"] - segment_to_letter["d"] - \
        segment_to_letter["f"] - segment_to_letter["g"]

    # reverse dictionary
    letter_to_segment = {}
    for k, v in segment_to_letter.items():
        letter_to_segment[v.pop()]=k

    # ok now we can finally compute the value!
    ret = 0
    for dig in output_digits:
        ret *= 10
        real_letters = ''
        for d in dig:
            real_letters += letter_to_segment[d]
        # dont forget to sort
        real_letters = ''.join(sorted(real_letters))
        ret += letters_to_int[real_letters]

    return ret


def boom_part2(input_val, DBG=True):
    ret = 0
    for ll in input_val:
        (signal_patterns, output_digits) = parse_line(ll, DBG)
        ret += compute_value(signal_patterns, output_digits, DBG)
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


tt1 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
tt1 = tt1.splitlines()
test_part1(tt1, 26, True)
test_part2(tt1, 61229, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d08.txt"
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

# PART 1 OK = 367
# PART 2 OK = 974512
