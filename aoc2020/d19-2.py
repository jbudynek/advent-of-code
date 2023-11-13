# coding: utf-8
import re
import sys
import time

import numpy as np


def parse_rule(ii, rules):
    rr = ii.split(":")
    nr = int(rr[0])
    if "|" in rr[1]:
        rrr = rr[1].split("|")
        lhs = np.asarray(re.findall(r"\d+", rrr[0]), dtype=np.int)
        rhs = np.asarray(re.findall(r"\d+", rrr[1]), dtype=np.int)
        rules[nr] = (lhs, rhs)
    elif '"' in rr[1]:
        rules[nr] = rr[1][2]
    else:
        lhs = np.asarray(re.findall(r"\d+", rr[1]), dtype=np.int)
        rules[nr] = lhs


def parse_rules_and_messages(input_val, DBG):
    rules = {}
    messages = []
    nl = len(input_val)
    idx = 0
    part = 0
    while idx < nl:
        ii = input_val[idx]
        if ii == "":
            part = part + 1
        elif part == 0:
            if ii.startswith("8:"):
                parse_rule("8: 42 | 42 8", rules)
            elif ii.startswith("11:"):
                parse_rule("11: 42 31 | 42 11 31", rules)
            else:
                parse_rule(ii, rules)
        elif part == 1:
            messages.append(ii)
        else:
            sys.exit("panic " + str(ii))
        idx = idx + 1

    if DBG:
        print(rules)
    return (rules, messages)


def match(message, m_pos, rules, r_idx, DBG):
    r = rules[r_idx]
    if m_pos >= len(message):  # too far
        return (False, m_pos)
    if isinstance(r, str):  # character
        ret = r == message[m_pos]
        return (ret, m_pos + 1)
    elif isinstance(r, tuple):  # N rules | P rules
        # test first set of N rules
        (ret_b, ret_p) = test_n_rules(message, r[0], r_idx, m_pos, rules, DBG)
        if ret_b:
            return (ret_b, ret_p)

        # test second set of P rules
        (ret_b, ret_p) = test_n_rules(message, r[1], r_idx, m_pos, rules, DBG)
        if ret_b:
            return (ret_b, ret_p)

        # no match
        return (False, m_pos)

    else:  # N rules
        (ret_b, ret_p) = test_n_rules(message, r, r_idx, m_pos, rules, DBG)
        return (ret_b, ret_p)

    return (False, -1)


def test_n_rules(message, r, r_idx, m_pos, rules, DBG):
    rrr = 0
    cur_m_pos = m_pos
    while rrr < len(r):
        mm1 = False
        (mm1, new_m_pos) = match(message, cur_m_pos, rules, r[rrr], DBG)
        if not mm1:
            return (False, m_pos)
        cur_m_pos = new_m_pos
        rrr = rrr + 1
    return (True, cur_m_pos)


def boom(input_val, DBG=True):
    (rules, messages) = parse_rules_and_messages(input_val, DBG)

    ret = 0
    for message in messages:
        if DBG:
            print(message)
        # 8 11 ...
        # 8 matches 42 p times
        # 11 matches 42 k times and 31 k times
        # 42{p} 42{k} 31{k} p>0 and k>=0
        # 42{n} 31{k} n>1 and k>0 and k<n

        # count numbers of matches to rule 42
        mm = True
        cur_m_pos = 0
        nb_42 = 0
        while mm and (cur_m_pos < len(message)):
            mm = False
            (mm, m_pos) = match(message, cur_m_pos, rules, 42, DBG)
            if mm:
                nb_42 = nb_42 + 1
                cur_m_pos = m_pos

        # count numbers of matches to rule 31
        mm = True
        nb_31 = 0
        while mm and (cur_m_pos < len(message)):
            mm = False
            (mm, m_pos) = match(message, cur_m_pos, rules, 31, DBG)
            if mm:
                nb_31 = nb_31 + 1
                cur_m_pos = m_pos

        # check numbers and final position
        if nb_42 > 1 and nb_31 > 0 and nb_31 < nb_42 and cur_m_pos == len(message):
            ret = ret + 1

    return ret


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


t1 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


tt1 = t1.splitlines()
test(tt1, 12, True)
# sys.exit()

INPUT_FILE = "input-d19.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)
print(ret)

# part 2 = 389
