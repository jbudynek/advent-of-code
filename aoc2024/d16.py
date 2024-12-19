import heapq

ipt = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".split(
    "\n"
)

ipt = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".split(
    "\n"
)

ipt = open("input-d16.txt").read().split("\n")


www = {}
start = (0, 0)
end = (0, 0)
max_x, max_y = len(ipt[0]), len(ipt)
for y, line in enumerate(ipt):
    for x, c in enumerate(line):
        if c != "#":
            if c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
            www[(x, y)] = c


def print_field_complex(field, path, x_min, x_max, y_min, y_max):
    for yy in range(y_min, y_max):
        ss = ""
        for xx in range(x_min, x_max):
            if (xx, yy) in path:
                ss += "O"
            elif (xx, yy) in field:
                ss += str(field[(xx, yy)])
            else:
                ss += "#"
        print(ss)


def dot_product(x, y, xx, yy):
    return x * xx + y * yy


def dijkstra_pos_dir_path(start_node, end_node, start_dir, field):
    visited_nodes_states = set()

    queue = [(0, start_node, start_dir, [start_node])]

    while len(queue) > 0:
        (shortest_path_len, (x, y), (dx, dy), path_so_far_0) = heapq.heappop(queue)
        if (x, y) == end_node:
            # print(shortest_path_len)
            # print_field_complex(field, path_so_far_0, 0, max_x, 0, max_y)
            return (x, y), (dx, dy), shortest_path_len

        if ((x, y), (dx, dy)) in visited_nodes_states:
            continue

        visited_nodes_states.add(((x, y), (dx, dy)))

        for ndx, ndy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if not ((dx == -ndx) and (dy == -ndy)):
                (nx, ny) = (x + ndx, y + ndy)
                if (nx, ny) in field:
                    score = 1
                    # if we turn, add 1000
                    if dot_product(dx, dy, ndx, ndy) == 0:
                        score += 1000
                    path_so_far = path_so_far_0.copy()
                    path_so_far.append((nx, ny))
                    heapq.heappush(
                        queue,
                        (
                            shortest_path_len + score,
                            (nx, ny),
                            (ndx, ndy),
                            path_so_far,
                        ),
                    )

    return None, None, None


_, _, r1 = dijkstra_pos_dir_path(start, end, (1, 0), www)


all_nodes = set()
for k in www.keys():
    pos_e, dir_e, len_path_1 = dijkstra_pos_dir_path(start, k, (1, 0), www)
    pos_e2, dir_e2, len_path_2 = dijkstra_pos_dir_path(pos_e, end, dir_e, www)

    if (
        len_path_1 is not None
        and len_path_2 is not None
        and len_path_1 + len_path_2 == r1
    ):
        all_nodes.add(k)

r2 = len(all_nodes)

print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 109516
# Part 2 solution: 568
