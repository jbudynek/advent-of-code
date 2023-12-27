# coding: utf-8
from collections import defaultdict, deque
from enum import Enum
from math import lcm

import matplotlib.pyplot as plt
import networkx as nx
from boilerplate import read_input_file, run_func, test_func


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class FlipFlop(Enum):
    OFF = 0
    ON = 1


def parse_modules(ipt):

    # create graph
    o2d = {}
    name2what = {}
    name2status = {}
    conv_input2mem = defaultdict(dict)
    name, what = "", ""
    for line in ipt:
        [o, d] = line.split(" -> ")
        if o[0] == "%" or o[0] == "&":
            name = o[1:]
            what = o[0]
        elif o == "broadcaster":
            name = o
            what = o
        elif o == "output":
            name = o
            what = o
        o2d[name] = d.split(", ")

        name2what[name] = what
        # default status for flipflops
        if what == "%":
            name2status[name] = FlipFlop.OFF

    # create nodes that only have inputs
    for vv in list(o2d.values()).copy():
        for dd in vv:
            if dd not in name2what:
                name2what[dd] = dd
                pass

    # create upstream mems for &s with default status
    for n, w in name2what.items():
        if w == "&":
            for o, d in o2d.items():
                if n in d:
                    conv_input2mem[n][o] = Pulse.LOW

    return o2d, name2what, name2status, conv_input2mem


def press_button(o2d, name2what, name2status, conv_input2mem, count_pulse):

    # (Pulse, origin, dest)
    todo = deque()
    todo.append((Pulse.LOW, None, "broadcaster"))
    count_pulse[Pulse.LOW] += 1

    # remember what is done to send it back
    done = deque()

    while len(todo) > 0:

        doing = todo.popleft()
        doing_pulse = doing[0]
        doing_origin = doing[1]
        doing_module = doing[2]
        # if doing_module=="rx":
        #    print(doing)
        # if doing_module == "rx" and doing_pulse == Pulse.LOW:
        #    return o2d, name2what, name2status, conv_input2mem, -1
        if doing_module == "broadcaster":
            for d in o2d["broadcaster"]:
                todo.append((doing_pulse, "broadcaster", d))
                count_pulse[doing_pulse] += 1

        elif name2what[doing_module] == "%":  # flip flop
            if doing_pulse == Pulse.HIGH:
                pass
            else:
                if name2status[doing_module] == FlipFlop.ON:
                    name2status[doing_module] = FlipFlop.OFF
                    for d in o2d[doing_module]:
                        todo.append((Pulse.LOW, doing_module, d))
                        count_pulse[Pulse.LOW] += 1
                elif name2status[doing_module] == FlipFlop.OFF:
                    name2status[doing_module] = FlipFlop.ON
                    for d in o2d[doing_module]:
                        todo.append((Pulse.HIGH, doing_module, d))
                        count_pulse[Pulse.HIGH] += 1
        elif name2what[doing_module] == "&":  # conv

            conv_input2mem[doing_module][doing_origin] = doing_pulse

            all_high = True
            for o in conv_input2mem[doing_module]:
                if conv_input2mem[doing_module][o] == Pulse.LOW:
                    all_high = False

            for d in o2d[doing_module]:
                if all_high:
                    todo.append((Pulse.LOW, doing_module, d))
                    count_pulse[Pulse.LOW] += 1
                else:
                    todo.append((Pulse.HIGH, doing_module, d))
                    count_pulse[Pulse.HIGH] += 1

        done.append(doing)

    return o2d, name2what, name2status, conv_input2mem, count_pulse, done


def boom_part1(ipt, DBG=True):
    o2d, name2what, name2status, conv_input2mem = parse_modules(ipt)

    count_pulse = defaultdict(int)

    for _ in range(1000):
        o2d, name2what, name2status, conv_input2mem, count_pulse, _ = press_button(
            o2d, name2what, name2status, conv_input2mem, count_pulse
        )

    ret = count_pulse[Pulse.HIGH] * count_pulse[Pulse.LOW]
    return ret


def boom_part2(ipt, DBG=True):

    o2d, name2what, name2status, conv_input2mem = parse_modules(ipt)

    if DBG:
        G = nx.Graph()
        for k, v in o2d.items():
            for d in v:
                G.add_edge(name2what[k] + k, name2what[d] + d)

        nx.draw_networkx(G, font_size=10, node_size=400)
        plt.draw()
        plt.savefig("d20-graph.png")

    # looking at the graph shows there are 4 distinct parts
    # looking at the input shows that conjunction vd goes to rx
    # and that conjunctions rd, bt, fv, pr go to vd
    # look for when those 4 conjunctions output a high pulse and suppose it's
    # cyclic, so do a lcm of all

    count_pulse = defaultdict(int)

    conjunctions = ["rd", "bt", "fv", "pr"]
    count_conj = {}

    nb_butt = 0
    while True:
        nb_butt += 1
        o2d, name2what, name2status, conv_input2mem, count_pulse, done = press_button(
            o2d, name2what, name2status, conv_input2mem, count_pulse
        )
        for d in done:
            if d[1] in conjunctions and d[0] == Pulse.HIGH:
                if DBG:
                    print(nb_butt, d)
                if not d[1] in count_conj:
                    count_conj[d[1]] = nb_butt
                if len(count_conj) == len(conjunctions):
                    return lcm(*count_conj.values())


# Test cases
#############


ipt_test1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".splitlines()
test_func(boom_part1, ipt_test1, 32000000, True)


ipt_test1 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
test_func(boom_part1, ipt_test1, 11687500, True)

# test_func(boom_part2, ipt_test1, -1, True)

# Real data
############

ipt_puzzle = read_input_file("input-d20.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 788848550
# Part 2 solution: 228300182686739
