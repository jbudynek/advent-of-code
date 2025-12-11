import networkx as nx

ipt_test = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""".splitlines()

ipt_test2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test
# ipt = ipt_test2

G = nx.DiGraph()

for line in ipt:
    parts = line.split(" ")
    from_node = parts[0][:-1]
    for i in range(1, len(parts)):
        to_node = parts[i]
        G.add_edge(from_node, to_node)

# traverse graph with memoisation

CACHE = {}


def count_paths(current_node, end_node, G, seen_dac, seen_fft):
    if (current_node, seen_dac, seen_fft) in CACHE:
        return CACHE[(current_node, seen_dac, seen_fft)]
    if current_node == end_node:
        if seen_dac and seen_fft:
            return 1
        else:
            return 0
    if current_node == "dac":
        seen_dac = True
    if current_node == "fft":
        seen_fft = True

    ret = 0
    for node in G.neighbors(current_node):
        d = count_paths(node, end_node, G, seen_dac, seen_fft)
        CACHE[(current_node, seen_dac, seen_fft)] = d
        ret += d

    CACHE[(current_node, seen_dac, seen_fft)] = ret

    return ret


r1 = count_paths("you", "out", G, True, True)
r2 = count_paths("svr", "out", G, False, False)


print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 494
# Part 2 solution: 296006754704850
