# coding: utf-8
import re
from collections import defaultdict

from boilerplate import read_input_file, run_func, test_func

# Helpers
##########


def strings_to_int_array(line):
    ii = list(map(int, re.findall(r"-?\d+", line)))
    return ii


# Main function
################


def parse_rules(input_val, DBG=True):

    rules = {}  # store rules
    for line in input_val:
        if line.startswith("bot"):
            ll = line.split(" ")
            bot_id = ll[0] + ll[1]
            low = ll[5] + ll[6]
            high = ll[10] + ll[11]
            rules[bot_id] = (low, high)
    return rules


def apply_rule(bot_id, rules, state):
    st = state[bot_id]
    if len(st) == 2:
        low = min(st)
        high = max(st)
        if low == 17 and high == 61:
            print(low, high, bot_id)
        if low == 2 and high == 5:
            print(low, high, bot_id)
        bot_id_low = rules[bot_id][0]
        state[bot_id_low].append(low)
        apply_rule(bot_id_low, rules, state)
        bot_id_high = rules[bot_id][1]
        state[bot_id_high].append(high)
        apply_rule(bot_id_high, rules, state)


def apply_all_rules(input_val, rules):
    state = defaultdict(list)

    for line in input_val:
        if line.startswith("value"):
            ii = strings_to_int_array(line)
            bot_id = "bot" + str(ii[1])
            st = state[bot_id]
            st.append(ii[0])
            apply_rule(bot_id, rules, state)

    return state


def boom_part2(input_val, DBG=True):
    rules = parse_rules(input_val, DBG)
    state = apply_all_rules(input_val, rules)
    return state["output0"][0] * state["output1"][0] * state["output2"][0]


# Test cases
#############


t1 = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""
tt1 = t1.splitlines()
test_func(boom_part2, tt1, -1, True)

# Real data
############

puzzle_input = read_input_file("input-d10.txt")

# part 1 & 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 157
# PART 2 OK = 1085
