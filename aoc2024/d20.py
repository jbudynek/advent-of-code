import networkx as nx

ipt = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""".split(
    "\n"
)

ipt = open("input-d20.txt").read().split("\n")

www = {}
start = complex(0, 0)
end = complex(0, 0)
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        if c != "#":
            if c == "S":
                start = complex(x, y)
            elif c == "E":
                end = complex(x, y)
            www[complex(x, y)] = c


dirs4 = [complex(0, 1) ** i for i in range(4)]


G = nx.Graph()
for z, v in www.items():
    for dz in dirs4:
        nz = z + dz
        if nz in www:
            G.add_edge(z, nz)

all_shortest_paths_len: dict[complex, dict[complex, int]] = {}

longest_path = nx.shortest_path(G, source=start, target=end)
longest_len = len(longest_path) - 1

all_shortest_paths_len[start] = {}
all_shortest_paths_len[start][end] = longest_len


def get_all_shortest_paths_len(s, e, graph, sh_p_len_dict):
    if not (s in sh_p_len_dict):
        sh_p_len_dict[s] = {}
    if not (e in sh_p_len_dict[s]):
        shp = nx.shortest_path(graph, source=s, target=e)
        sh_p_len_dict[s][e] = len(shp) - 1
    return sh_p_len_dict[s][e]


def manhattan_distance(c1, c2):
    return int(abs(c1.real - c2.real) + abs(c1.imag - c2.imag))


def boom(min_manhattan_dist, max_manhattan_dist):
    best_savings = {}
    for i, z0 in enumerate(longest_path):
        if i % 1000 == 0:
            print(f"{i}/{longest_len}")
        for j in range(i, longest_len + 1):
            z1 = longest_path[j]
            if min_manhattan_dist <= manhattan_distance(z0, z1) <= max_manhattan_dist:
                d_s_1 = get_all_shortest_paths_len(start, z0, G, all_shortest_paths_len)
                d_s_2 = get_all_shortest_paths_len(z1, end, G, all_shortest_paths_len)
                rr = d_s_1 + manhattan_distance(z0, z1) + d_s_2
                if rr < longest_len:
                    new_saving = longest_len - rr
                    if new_saving not in best_savings:
                        best_savings[new_saving] = set()
                    best_savings[new_saving].add((z0, z1))
    return best_savings


best_savings1 = boom(2, 2)  # part 1
best_savings2 = boom(0, 20)  # part 1

r1 = sum([len(v) for k, v in best_savings1.items() if k >= 100])
r2 = sum([len(v) for k, v in best_savings2.items() if k >= 100])


print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")


# Part 1 solution: 1499
# Part 2 solution: 1027164
