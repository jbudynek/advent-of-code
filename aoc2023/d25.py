# coding: utf-8
import matplotlib.pyplot as plt
import networkx as nx
from boilerplate import read_input_file, run_func, test_func

# You can try to brute force and remove all possible triplets of edges.
# That works for the test dataset.
# You can also simply draw the graph, and the answer will be obvious.


def parse_graph(ipt) -> nx.Graph:
    G = nx.Graph()
    for ll in ipt:
        [o, d] = ll.split(": ")
        for dd in d.split():
            G.add_edge(o, dd)
    return G


def search_which_edges(g):
    ll = len(g.edges)
    edge_list = list(g.edges).copy()
    for i in range(ll):
        for j in range(i + 1, ll):
            for k in range(j + 1, ll):
                g2 = g.copy()
                g2.remove_edge(edge_list[i][0], edge_list[i][1])
                g2.remove_edge(edge_list[j][0], edge_list[j][1])
                g2.remove_edge(edge_list[k][0], edge_list[k][1])
                cc = list(nx.connected_components(g2))
                if len(cc) == 2:
                    return len(cc[0]) * len(cc[1])
    quit("did not find which edges to remove")


def draw_graph(g):
    nx.draw_networkx(g, font_size=10, node_size=400)
    plt.draw()
    plt.savefig("d25-graph.png")

    g.remove_edge("zpc", "xvp")
    g.remove_edge("vfs", "dhl")
    g.remove_edge("nzn", "pbq")
    cc = nx.number_connected_components(g)
    if cc == 2:
        cc = list(nx.connected_components(g))
        return len(cc[0]) * len(cc[1])

    quit("did not find which edges to remove")


def boom_part1(ipt, DBG=True):
    g = parse_graph(ipt)

    if DBG:
        return search_which_edges(g)

    return draw_graph(g)


# Test cases
#############


ipt_test1 = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines()
test_func(boom_part1, ipt_test1, 54, True)

# Real data
############

ipt_puzzle = read_input_file("input-d25.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)


print("******")
print(f"# Part 1 solution: {result1}")

quit()

# Part 1 solution: 562978
# Part 2 solution: no part 2 on dec 25th
