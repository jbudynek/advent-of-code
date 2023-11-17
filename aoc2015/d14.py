# coding: utf-8

from collections import defaultdict

from boilerplate import read_input_file, run_func, test_func

# Main function
##########


def build_world(input_val):
    names = []
    speeds = []
    time_fly = []
    time_rest = []

    for line in input_val:
        ll = line.split()
        names.append(ll[0])
        speeds.append(int(ll[3]))
        time_fly.append(int(ll[6]))
        time_rest.append(int(ll[13]))

    return names, speeds, time_fly, time_rest


def get_distances_after_duration(sec, names, speeds, time_fly, time_rest):
    l_names = len(names)

    distances = defaultdict(int)

    for i in range(l_names):
        cur_name = names[i]

        total_duration_cycle = time_fly[i] + time_rest[i]
        nb_full_cycles = sec // total_duration_cycle
        dist = nb_full_cycles * speeds[i] * time_fly[i]
        time_left = sec % total_duration_cycle
        if time_left <= time_fly[i]:
            dist += time_left * speeds[i]
        else:
            dist += speeds[i] * time_fly[i]

        distances[cur_name] = dist

    return distances


def boom_part1(input_val, DBG=True):
    names, speeds, time_fly, time_rest = build_world(input_val)
    sec = 2503
    distances = get_distances_after_duration(sec, names, speeds, time_fly, time_rest)
    return max(distances.values())


def boom_part2(input_val, DBG=True):
    names, speeds, time_fly, time_rest = build_world(input_val)
    max_sec = 2503
    scores = defaultdict(int)
    for sec in range(1, max_sec + 1):
        distances = get_distances_after_duration(
            sec, names, speeds, time_fly, time_rest
        )
        max_dist = max(distances.values())
        max_keys = [k for k, v in distances.items() if v == max_dist]
        for k in max_keys:
            scores[k] += 1
    return max(scores.values())


# Test cases
##########

tt1_all = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
tt1 = tt1_all.splitlines()
test_func(boom_part1, tt1, 2660, True)  # 1120 for 1000 sec

test_func(boom_part2, tt1, 1564, True)  # 689 for 1000 sec

# Real data
##########

puzzle_input = read_input_file("aoc2015/input-d14.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)


print("******")
print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

quit()

# PART 1 OK = 2655
# PART 2 OK = 1059
