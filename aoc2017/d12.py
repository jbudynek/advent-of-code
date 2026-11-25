# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# The programs and their pipes form an undirected graph.
# - Part 1: depth-first search (DFS, using a stack) from program 0; the size of
#   the set of visited programs is the size of its group.
# - Part 2: pick any program not yet assigned to a group, compute its group with
#   the same DFS, remove that group from the remaining programs and increment
#   the counter; repeat until nothing is left.
#   The final counter is the number of connected components (groups).

ipt_test = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    graph = {}
    for line in ipt.splitlines():
        a, b = line.split(" <-> ")
        graph[int(a)] = [int(x) for x in b.split(", ")]
    return graph


def group(graph, start=0):
    seen = {start}
    stack = [start]
    while stack:
        n = stack.pop()
        for m in graph[n]:
            if m not in seen:
                seen.add(m)
                stack.append(m)
    return seen


def count_groups(graph):
    remaining = set(graph)
    n = 0
    while remaining:
        remaining -= group(graph, next(iter(remaining)))
        n += 1
    return n


# test
g_test = parse(ipt_test)
r_test1 = len(group(g_test))
r_test2 = count_groups(g_test)
print(f"# Test part 1: {r_test1} (expected 6)")
print(f"# Test part 2: {r_test2} (expected 2)")
assert r_test1 == 6
assert r_test2 == 2

g = parse(ipt_puzzle)
r1 = len(group(g))
r2 = count_groups(g)
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 378
# Part 2 solution: 204
