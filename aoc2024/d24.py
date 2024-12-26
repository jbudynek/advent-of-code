# For this puzzle, part 1 was OK, but I confess referring to the reddit thread
# for part 2. I did not recognize an adder circuit. Once I found this out I
# proceeded as follows:
# Build a graph using graphviz (neat!)
# Inspect graph and see which z's do not have XORs as input (they have to,
# except for the last one z45)
# This gave me: z12, z21 and z33
# Then I used a function to find which wire to swap them with
# (see find_swap_for_known_wire)
# --> (z12, vdc) and (z21, nhn)
# but it did not work right away for z33, something had to be swapped before
# (meaning in bits lower than 33, but higher than 21)
# So I looked up a swap from bit 22 to 33 (see find_swap) --> (tvb, khg)
# Then z33 again --> (gst, z33)
# That was very challenging!
# The code is very messy.

import graphviz
import numpy as np

seed = 3141592  # Knuth's Pi

np.random.seed(seed)

ipt_1_4 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""".split(
    "\n\n"
)

ipt_1_2024 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""".split(
    "\n\n"
)

ipt = ipt_1_4
ipt = ipt_1_2024

ipt = open("input-d24.txt").read().strip().split("\n\n")

r1, r2 = 0, ""

# Build all structures using input data


def initialize(lines):

    wire_to_value: dict[str, int] = {}
    node_idx_to_op: dict[int, str] = {}
    wires_in_to_node_idx: dict[tuple, int] = {}
    node_idx_to_wires_in: dict[int, tuple] = {}
    node_idx_to_wire_out: dict[int, str] = {}
    wire_out_to_node_idx: dict[str, int] = {}

    node_idx = 0
    for line in lines.split("\n"):
        ll = line.split()
        node_idx_to_op[node_idx] = ll[1]
        wires_in_to_node_idx[(ll[0], ll[2])] = node_idx
        node_idx_to_wires_in[node_idx] = (ll[0], ll[2])
        node_idx_to_wire_out[node_idx] = ll[4]
        wire_out_to_node_idx[ll[4]] = node_idx
        if ll[0] not in wire_to_value:
            wire_to_value[ll[0]] = -1
        if ll[2] not in wire_to_value:
            wire_to_value[ll[2]] = -1
        if ll[4] not in wire_to_value:
            wire_to_value[ll[4]] = -1
        node_idx += 1

    return (
        wire_to_value,
        node_idx_to_op,
        wires_in_to_node_idx,
        node_idx_to_wires_in,
        node_idx_to_wire_out,
        wire_out_to_node_idx,
    )


# Run the circuit, initial input (x and y) is in "wire_to_value"
# if more than 1000 rounds, bail out, there must be a loop
def evaluate(wire_to_value, node_idx_to_op, node_idx_to_wires_in, node_idx_to_wire_out):
    count_rounds = 0
    done = False
    while not done:
        count_rounds += 1
        if count_rounds == 1000:
            return -1
        done = True

        for node_idx, op in node_idx_to_op.items():
            (wire_in_lhs, wire_in_rhs) = node_idx_to_wires_in[node_idx]
            wire_out = node_idx_to_wire_out[node_idx]

            lhs = wire_to_value[wire_in_lhs]
            rhs = wire_to_value[wire_in_rhs]
            out_v = wire_to_value[wire_out]

            if out_v == -1:
                done = False

            if lhs != -1 and rhs != -1 and out_v == -1:
                ret = -1
                if op == "AND":
                    ret = lhs & rhs
                elif op == "OR":
                    ret = lhs | rhs
                elif op == "XOR":
                    ret = lhs ^ rhs
                wire_to_value[wire_out] = ret
                done = False

    i = 0
    done = False
    binary_output = ""
    while not done:
        key = "z" + format(i, "02d")
        if key in wire_to_value:
            binary_output = str(wire_to_value[key]) + binary_output
        else:
            done = True
        i += 1

    z = int(binary_output, 2)
    return z


# get number of bits of input x,y and output z
def get_max_xyz(wire_to_value):
    max_x, max_y, max_z = 0, 0, 0
    for wire in wire_to_value.keys():
        if wire[0] == "x" and int(wire[1:]) > max_x:
            max_x = int(wire[1:])
        if wire[0] == "y" and int(wire[1:]) > max_y:
            max_y = int(wire[1:])
        if wire[0] == "z" and int(wire[1:]) > max_z:
            max_z = int(wire[1:])
    return max_x, max_y, max_z


# set an int value into proper binary inputs x,y
def set_xy(val, max_num, num_char, wire_to_value):
    for i in range(max_num + 1):
        to_set = val % 2
        wire_to_value[num_char + format(i, "02d")] = to_set
        val = val // 2
    return wire_to_value


# get int value out of binary registers x,y or z
def get_xyz(num_char, wire_to_value):
    i = 0
    done = False
    binary_out = ""
    while not done:
        key = num_char + format(i, "02d")
        if key in wire_to_value:
            binary_out = str(wire_to_value[key]) + binary_out
        else:
            done = True
        i += 1

    ret = int(binary_out, 2)
    return ret


# to reset all the wires (in between rounds)
def reset_wire_to_value(wire_to_value):
    for k in wire_to_value.keys():
        wire_to_value[k] = -1
    return wire_to_value


# set x and y, run circuit, and see if result is really the expected sum
def correct_sum(x, y, wire_to_value, node_idx_to_wire_out, max_x, max_y):
    wire_to_value = reset_wire_to_value(wire_to_value)
    wire_to_value = set_xy(x, max_x, "x", wire_to_value)
    wire_to_value = set_xy(y, max_y, "y", wire_to_value)

    xxx = get_xyz("x", wire_to_value)
    yyy = get_xyz("y", wire_to_value)
    z = evaluate(
        wire_to_value, node_idx_to_op, node_idx_to_wires_in, node_idx_to_wire_out
    )
    if z == -1:
        return False
    elif z != xxx + yyy:
        return False
    else:
        return True


# carry out numerous additions, for random x and y values up to 2**bits
def test(bits, wire_to_value, node_idx_to_wire_out, max_x, max_y, tries=100):
    for _ in range(tries):
        x = np.random.randint(0, pow(2, bits) - 1)
        y = np.random.randint(0, pow(2, bits) - 1)
        if not correct_sum(x, y, wire_to_value, node_idx_to_wire_out, max_x, max_y):
            return False
    return True


# if one wire is known to be swapped, find the other wire, with x,y on nb_bits
def find_swap_for_known_wire(
    fix,
    nb_bits,
    wire_to_value,
    node_idx_to_wire_out,
    wire_out_to_node_idx,
    max_x,
    max_y,
):
    idx_node = fix
    for _, jdx_node in enumerate(node_idx_to_wire_out.keys()):
        node_idx_to_wire_out_swap = node_idx_to_wire_out.copy()
        node_idx_to_wire_out_swap[idx_node], node_idx_to_wire_out_swap[jdx_node] = (
            node_idx_to_wire_out_swap[jdx_node],
            node_idx_to_wire_out_swap[idx_node],
        )
        w1, w2 = (
            node_idx_to_wire_out_swap[idx_node],
            node_idx_to_wire_out_swap[jdx_node],
        )
        if test(nb_bits, wire_to_value, node_idx_to_wire_out_swap, max_x, max_y, 500):
            node_idx_to_wire_out = node_idx_to_wire_out_swap.copy()
            wire_out_to_node_idx[w1], wire_out_to_node_idx[w2] = (
                wire_out_to_node_idx[w2],
                wire_out_to_node_idx[w1],
            )
            return (idx_node, jdx_node, node_idx_to_wire_out, wire_out_to_node_idx)


# find two wires to be swapped, with x,y on nb_bits
def find_swap(
    nb_bits, wire_to_value, node_idx_to_wire_out, wire_out_to_node_idx, max_x, max_y
):
    for i, idx_node in enumerate(node_idx_to_wire_out.keys()):
        if i % 25 == 0:
            print(i, "/", len(node_idx_to_wire_out.keys()))
        for _, jdx_node in enumerate(node_idx_to_wire_out.keys()):
            if jdx_node <= idx_node:
                continue
            node_idx_to_wire_out_swap = node_idx_to_wire_out.copy()
            node_idx_to_wire_out_swap[idx_node], node_idx_to_wire_out_swap[jdx_node] = (
                node_idx_to_wire_out_swap[jdx_node],
                node_idx_to_wire_out_swap[idx_node],
            )
            w1, w2 = (
                node_idx_to_wire_out_swap[idx_node],
                node_idx_to_wire_out_swap[jdx_node],
            )
            if test(
                nb_bits, wire_to_value, node_idx_to_wire_out_swap, max_x, max_y, 500
            ):
                node_idx_to_wire_out = node_idx_to_wire_out_swap.copy()
                wire_out_to_node_idx[w1], wire_out_to_node_idx[w2] = (
                    wire_out_to_node_idx[w2],
                    wire_out_to_node_idx[w1],
                )
                return (idx_node, jdx_node, node_idx_to_wire_out, wire_out_to_node_idx)


# Part 1 - compute value from input file

(
    wire_to_value,
    node_idx_to_op,
    wires_in_to_node_idx,
    node_idx_to_wires_in,
    node_idx_to_wire_out,
    wire_out_to_node_idx,
) = initialize(ipt[1])

max_x, max_y, max_z = get_max_xyz(wire_to_value)

for line in ipt[0].split("\n"):
    ll = line.split(": ")
    wire_to_value[ll[0]] = int(ll[1])

r1 = evaluate(wire_to_value, node_idx_to_op, node_idx_to_wires_in, node_idx_to_wire_out)

print(f"# Part 1 solution: {r1}")

# Part 2
# Build Graph

graph = graphviz.Digraph()
for node_idx, op in node_idx_to_op.items():
    (wire_in1, wire_in2) = node_idx_to_wires_in[node_idx]
    wire_out = node_idx_to_wire_out[node_idx]

    graph.edge(wire_in1, wire_out, f"{op}")
    graph.edge(wire_in2, wire_out, f"{op}")
graph.render("241224_adder", format="png")
graph.render("241224_adder", format="pdf")

# Graph reveals that z12, z21 and z33 must be swapped.
# Find all swaps with those, and the remaining swap.
# Note that we always test 2 more bits, to avoid carry errors.
# The exact sequence of events was found by trial and error.

swaps = []


def swap_lookup(
    nb_bits, wire_to_value, node_idx_to_wire_out, wire_out_to_node_idx, max_x, max_y
):
    fix = wire_out_to_node_idx["z" + format(nb_bits, "02d")]
    (g1, g2, node_idx_to_wire_out, wire_out_to_node_idx) = find_swap_for_known_wire(
        fix,
        nb_bits + 2,
        wire_to_value,
        node_idx_to_wire_out,
        wire_out_to_node_idx,
        max_x,
        max_y,
    )
    print(g1, g2, node_idx_to_wire_out[g1], node_idx_to_wire_out[g2])
    return (
        node_idx_to_wire_out[g1],
        node_idx_to_wire_out[g2],
        node_idx_to_wire_out,
        wire_out_to_node_idx,
    )


s1, s2, node_idx_to_wire_out, wire_out_to_node_idx = swap_lookup(
    12, wire_to_value, node_idx_to_wire_out, wire_out_to_node_idx, max_x, max_y
)
swaps.extend([s1, s2])

s1, s2, node_idx_to_wire_out, wire_out_to_node_idx = swap_lookup(
    21, wire_to_value, node_idx_to_wire_out, wire_out_to_node_idx, max_x, max_y
)
swaps.extend([s1, s2])

for nb_bits in range(22, 33):
    if not test(nb_bits, wire_to_value, node_idx_to_wire_out, max_x, max_y):
        (g1, g2, node_idx_to_wire_out, wire_out_to_node_idx) = find_swap(
            nb_bits + 2,
            wire_to_value,
            node_idx_to_wire_out,
            wire_out_to_node_idx,
            max_x,
            max_y,
        )
        print(g1, g2, node_idx_to_wire_out[g1], node_idx_to_wire_out[g2])
        swaps.append(node_idx_to_wire_out[g1])
        swaps.append(node_idx_to_wire_out[g2])

s1, s2, node_idx_to_wire_out, wire_out_to_node_idx = swap_lookup(
    33, wire_to_value, node_idx_to_wire_out, wire_out_to_node_idx, max_x, max_y
)
swaps.extend([s1, s2])

# concatenate

r2 = ",".join(sorted(swaps))

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 51410244478064
# Part 2 solution: gst,khg,nhn,tvb,vdc,z12,z21,z33
