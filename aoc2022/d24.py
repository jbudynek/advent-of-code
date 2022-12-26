# coding: utf-8
import sys

from boilerplate import read_input_file, run_func, test_func


def get_bounds_24(tracks, DBG):
    coords = tracks.keys()
    x_min = int(min(coords, key=lambda t: t[0])[0])
    x_max = int(max(coords, key=lambda t: t[0])[0])
    y_min = int(min(coords, key=lambda t: t[1])[1])
    y_max = int(max(coords, key=lambda t: t[1])[1])
    return (x_min, x_max, y_min, y_max)


def print_field_24(xyids, border, DBG=True):
    if DBG:
        print(xyids)

    (x_min, x_max, y_min, y_max) = get_bounds_24(xyids, DBG)

    x_min -= 1
    x_max += 1
    y_min -= 1
    y_max += 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                li = xyids[(xx, yy)]
                if len(li) == 1:
                    ss += li[0]
                else:
                    ss += str(len(li))
            elif (xx, yy) in border:
                ss += border[(xx, yy)]
            else:
                ss += " "
        print(ss)


def create_field_and_border(input):

    x_min, x_max, y_min, y_max = 0, len(input[0]), 0, len(input)

    field = {}
    border = {}

    y = -1
    for line in input:
        y += 1
        x = -1
        for c in line:
            x += 1
            if c == ".":
                pass
            elif c == "#":
                border[(x, y)] = c
            else:
                field[(x, y)] = [c]

    border[(1, -1)] = "#"
    border[(x_max - 2, y_max)] = "#"

    return field, border, x_min, x_max, y_min, y_max


def tick(field, x_min, x_max, y_min, y_max):
    delta = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0),
    }
    new_field = {}
    for xy, lbliz in field.items():
        for bliz in lbliz:
            dbliz = delta[bliz]
            (nx, ny) = (xy[0] + dbliz[0], xy[1] + dbliz[1])
            if (nx > xy[0]) and (nx >= x_max - 1):
                nx = x_min + 1
            elif (nx < xy[0]) and (nx <= x_min):
                nx = x_max - 2
            elif (ny > xy[1]) and (ny >= y_max - 1):
                ny = y_min + 1
            elif (ny < xy[1]) and (ny <= y_min):
                ny = y_max - 2
            nxy = (nx, ny)
            if nxy not in new_field:
                new_field[nxy] = [bliz]
            else:
                new_field[nxy].append(bliz)
    return new_field


def shortest_path_bfs(start, end, field, border, x_min, x_max, y_min, y_max):
    time = 0
    queue = [start]
    while True:
        new_field = tick(field, x_min, x_max, y_min, y_max)
        time += 1
        next_queue = set()
        while len(queue) > 0:
            pos = queue.pop(0)
            if pos == end:
                return (time - 1, field)
            neigh = []
            dirs = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
            for dir in dirs:
                nxy = (pos[0] + dir[0], pos[1] + dir[1])
                if nxy not in new_field and nxy not in border:
                    neigh.append(nxy)
            next_queue.update(neigh)
        queue = list(next_queue)
        field = new_field


def boom_part1(input_val, DBG=True):
    field, border, x_min, x_max, y_min, y_max = create_field_and_border(input_val)

    if DBG:
        print_field_24(field, border, DBG)

    start = (1, 0)
    end = (x_max - 2, y_max - 1)
    ret, _ = shortest_path_bfs(start, end, field, border, x_min, x_max, y_min, y_max)

    return ret


def boom_part2(input_val, DBG=True):
    field, border, x_min, x_max, y_min, y_max = create_field_and_border(input_val)

    if DBG:
        print_field_24(field, border, DBG)

    start = (1, 0)
    end = (x_max - 2, y_max - 1)

    ret0, nf1 = shortest_path_bfs(start, end, field, border, x_min, x_max, y_min, y_max)
    ret1, nf2 = shortest_path_bfs(end, start, nf1, border, x_min, x_max, y_min, y_max)
    ret2, _ = shortest_path_bfs(start, end, nf2, border, x_min, x_max, y_min, y_max)

    return ret0 + ret1 + ret2


# Test cases
##########


t1 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 18, True)
# sys.exit()
test_func(boom_part2, tt1, 54, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d24.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

sys.exit()

# PART 1 OK = 251
# PART 2 OK = 758
