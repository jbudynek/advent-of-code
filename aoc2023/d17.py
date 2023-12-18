# coding: utf-8
import heapq

from boilerplate import read_input_file, run_func, test_func


def parse_field(input):

    x_min, x_max, y_min, y_max = 0, len(input[0]), 0, len(input)

    field = {(x, y): int(input[y][x]) for y in range(y_max) for x in range(x_max)}

    return field, x_min, x_max, y_min, y_max


############################

# it's a Dijkstra shortest path algorithm, but we store more than just
# the position.
# what we store is a tuple:
# (shortest path len - position - direction - steps already taken in direction)
# we use priority queue (heapq in python), the sorting is naturally done by
# the first element in the tuple
# then to remember what we visited before, we store
# (position - direction - steps already taken in the direction)


def dijkstra_pos_dir_len(start_node, end_node, field, min_turn, max_turn):
    visited_nodes_states = set()
    # note that we start with len 0, steps 0 and direction 0,0, this is the
    # only time we do that
    # (shortest path len - (position) - (direction) - steps taken)
    queue = [(0, start_node, (0, 0), 0)]

    while len(queue) > 0:
        # this gets the position to study: the one with the shortest path so far
        # (shortest path len - (position) - (direction) - steps taken)
        (shortest_path_len, (x, y), (dx, dy), steps_taken) = heapq.heappop(queue)
        if (x, y) == end_node:
            return shortest_path_len
        if ((x, y), (dx, dy), steps_taken) in visited_nodes_states:
            continue
        # note that we visited this state
        visited_nodes_states.add(((x, y), (dx, dy), steps_taken))
        # add step without turning if possible
        if steps_taken < max_turn and (dx, dy) != (0, 0):
            (nx, ny) = (x + dx, y + dy)
            if (nx, ny) in field:
                # push a new position to study
                heapq.heappush(
                    queue,
                    (
                        shortest_path_len + field[(nx, ny)],
                        (nx, ny),
                        (dx, dy),
                        steps_taken + 1,
                    ),
                )
        # add steps with turning if appropriate
        if (dx == 0 and dy == 0) or steps_taken >= min_turn:
            # try all directions except same and reverse
            for (ndx, ndy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if (ndx, ndy) != (dx, dy) and (ndx, ndy) != (-dx, -dy):
                    (nx, ny) = (x + ndx, y + ndy)
                    if (nx, ny) in field:
                        # push a new position to study
                        heapq.heappush(
                            queue,
                            (
                                shortest_path_len + field[(nx, ny)],
                                (nx, ny),
                                (ndx, ndy),
                                1,
                            ),
                        )


def boom_part1(ipt, DBG=True):
    field, _, x_max, _, y_max = parse_field(ipt)
    start = (0, 0)
    dest = (x_max - 1, y_max - 1)
    ret = dijkstra_pos_dir_len(start, dest, field, 0, 3)
    return ret


def boom_part2(ipt, DBG=True):
    field, _, x_max, _, y_max = parse_field(ipt)
    start = (0, 0)
    dest = (x_max - 1, y_max - 1)
    ret = dijkstra_pos_dir_len(start, dest, field, 4, 10)
    return ret


# Test cases
#############


ipt_test1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()
test_func(boom_part1, ipt_test1, 102, True)
test_func(boom_part2, ipt_test1, 94, True)

# Real data
############

ipt_puzzle = read_input_file("input-d17.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 1260
# Part 2 solution: 1416
