import networkx as nx

ipt_1_7 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""".split(
    "\n"
)

ipt = ipt_1_7

ipt = open("input-d23.txt").read().strip().split("\n")

net = nx.Graph()

for ll in ipt:
    nodes = ll.split("-")
    net.add_edge(nodes[0], nodes[1])


# part 1: use networkx.enumerate_all_cliques(net), it returns all cliques
# (group of n interconnected nodes), sorted by size.
r1 = 0
clic_clic = list(nx.enumerate_all_cliques(net))
for clique in clic_clic:
    if len(clique) == 3:
        for node in clique:
            if node[0] == "t":
                r1 += 1
                break

# part 2: the last clique of the list is the largest
all_nodes_in_biggest_clique = set(clic_clic[-1])

r2 = ",".join(sorted(list(all_nodes_in_biggest_clique)))

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1330
# Part 2 solution: hl,io,ku,pk,ps,qq,sh,tx,ty,wq,xi,xj,yp
