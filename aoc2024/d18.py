import heapq

ipt = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".split(
    "\n"
)
start = (0, 0)
end = (6, 6)
nb_bytes = 12

ipt = open("input-d18.txt").read().split("\n")
start = (0, 0)
end = (70, 70)
nb_bytes = 1024


www = set()
max_x, max_y = 0, 0
for i, line in enumerate(ipt):
    if i == nb_bytes:
        break
    xy = line.split(",")
    (x, y) = int(xy[0]), int(xy[1])
    www.add((x, y))


def dijkstra_pos_path(start_node, end_node, field, max_x, max_y):
    visited_nodes_states = set()
    queue = [(0, start_node, [start_node])]

    while len(queue) > 0:
        (shortest_path_len, (x, y), path_so_far) = heapq.heappop(queue)
        if (x, y) == end_node:
            return shortest_path_len
        if ((x, y)) in visited_nodes_states:
            continue
        visited_nodes_states.add(((x, y)))
        for (ndx, ndy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            (nx, ny) = (x + ndx, y + ndy)
            if (nx, ny) not in field and (0 <= nx <= max_x) and (0 <= ny <= max_y):
                score = 1
                path_so_far = path_so_far.copy()
                path_so_far.append((nx, ny))
                heapq.heappush(
                    queue,
                    (
                        shortest_path_len + score,
                        (nx, ny),
                        path_so_far,
                    ),
                )


r1 = dijkstra_pos_path(start, end, www, end[0], end[1])

r2 = ""
for i in range(nb_bytes, len(ipt)):
    line = ipt[i]
    xy = line.split(",")
    (x, y) = int(xy[0]), int(xy[1])
    www.add((x, y))
    r2 = dijkstra_pos_path(start, end, www, end[0], end[1])
    if r2 is None:
        r2 = str(x) + "," + str(y)
        break


print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 408
# Part 2 solution: 0
