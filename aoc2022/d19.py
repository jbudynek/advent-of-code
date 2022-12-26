# coding: utf-8
import collections
import copy
import re
import sys

from boilerplate import read_input_file, run_func, test_func

# DFS with LRU cache
# works but really slow


def parse_blueprints(ipt):
    blueprints = {}

    for line in ipt:
        ll = line.split("Each")
        bp = {}
        idx = list(map(int, re.findall(r"-?\d+", ll[0])))[0]
        del ll[0]
        for p in ll:
            pp = p.split()
            robot = pp[0]
            costs = {}
            i = 3
            while i < len(pp):
                costs[pp[i + 1].strip(".")] = int(pp[i])
                i += 3
            bp[robot] = costs
        blueprints[idx] = bp
        print(bp)

    return blueprints


def can_build_bot(resources, bot, blueprint):
    costs = blueprint[bot]
    for stone, nb in costs.items():
        if stone not in resources:
            return False
        elif resources[stone] < nb:
            return False
    return True


def collect_resources(resources, bots):
    for bot, nb in bots.items():
        if bot not in resources:
            resources[bot] = 0
        resources[bot] += nb


def add_bot(resources, bots, stone, blueprint):
    if stone not in bots:
        bots[stone] = 0
    bots[stone] += 1

    costs = blueprint[stone]
    for ss, nb in costs.items():
        resources[ss] -= nb


def get_nb_geodes(resources):
    return resources["geode"]


class SimpleLRUCache:
    def __init__(self, size):
        self.size = size
        self.lru_cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.lru_cache.pop(key)
            self.lru_cache[key] = value
            return value
        except KeyError:
            return -1

    def containsKey(self, key):
        return key in self.lru_cache

    def put(self, key, value):
        try:
            self.lru_cache.pop(key)
        except KeyError:
            if len(self.lru_cache) >= self.size:
                self.lru_cache.popitem(last=False)
        self.lru_cache[key] = value

    def len(self):
        return len(self.lru_cache)


CACHE = SimpleLRUCache(10000000)
BEST_ANSWER = 0


def depth_first_search(remaining_minutes, resources, bots, blueprint):

    global BEST_ANSWER
    global CACHE

    key = (
        str(remaining_minutes)
        + "_"
        + str(tuple(sorted(resources.items())))
        + "_"
        + str(tuple(sorted(bots.items())))
    )
    if CACHE.containsKey(key):
        return CACHE.get(key)

    # if we don't create new robots,
    # here is the minimum number of geodes that we will create
    # if it's better than our current best,
    # then that's our new current best
    no_new_robot_answer = get_nb_geodes(resources) + bots["geode"] * remaining_minutes
    if no_new_robot_answer > BEST_ANSWER:
        BEST_ANSWER = no_new_robot_answer
        # print("- new best:", best)

    # if we create one additional geode robot each tick,
    # here is the maximal number of geodes that we will create
    # (n*(n+1)/2 geodes)
    # if it's lower that our current best,
    # then our current best is the absolute best and we can return
    max_new_robot_answer = no_new_robot_answer + (
        remaining_minutes * (remaining_minutes - 1) // 2
    )
    if max_new_robot_answer <= BEST_ANSWER:
        CACHE.put(key, BEST_ANSWER)
        return BEST_ANSWER

    stones = ["ore", "clay", "obsidian", "geode"]

    # depending on resources, try all creation possibilities

    # ore, clay, obsidian, geode
    all_nb_geode = []

    # start with geode robot, try backwards
    # if can build robot - build robot, collect, add geode and recurse
    for stone in reversed(stones):
        if can_build_bot(resources, stone, blueprint):
            res2 = copy.deepcopy(resources)
            bots2 = copy.deepcopy(bots)
            collect_resources(res2, bots2)
            add_bot(res2, bots2, stone, blueprint)
            nb_geode = depth_first_search(remaining_minutes - 1, res2, bots2, blueprint)
            all_nb_geode.append(nb_geode)

    # else collect and recurse
    res2 = copy.deepcopy(resources)
    bots2 = copy.deepcopy(bots)
    collect_resources(res2, bots2)
    nb_geode = depth_first_search(remaining_minutes - 1, res2, bots2, blueprint)
    all_nb_geode.append(nb_geode)

    CACHE.put(key, max(all_nb_geode))

    return max(all_nb_geode)


def boom_part1(input_val, DBG=True):
    global CACHE
    global BEST_ANSWER

    stones = ["ore", "clay", "obsidian", "geode"]

    blueprints = parse_blueprints(input_val)
    # parse blueprints
    # loop on blueprints

    bp = blueprints[1]
    resources = {k: 0 for k in stones}
    bots = {k: 0 for k in stones}
    bots["ore"] = 1

    ret = 0
    for idx, bp in blueprints.items():
        print("***", idx)
        CACHE = SimpleLRUCache(10000000)
        BEST_ANSWER = 0
        resources = {k: 0 for k in stones}
        bots = {k: 0 for k in stones}
        bots["ore"] = 1
        # dfs
        max_nb_g = depth_first_search(24, resources, bots, bp)
        # compute sumprod
        ret += idx * max_nb_g
        print(">", max_nb_g)

    return ret


def boom_part2(input_val, DBG=True):
    global CACHE
    global BEST_ANSWER

    stones = ["ore", "clay", "obsidian", "geode"]

    blueprints = parse_blueprints(input_val)
    # parse blueprints
    # loop on blueprints

    ret = 1
    for idx, bp in blueprints.items():
        if idx > 3:
            break
        print("***", idx)
        CACHE = SimpleLRUCache(10000000)
        BEST_ANSWER = 0
        resources = {k: 0 for k in stones}
        bots = {k: 0 for k in stones}
        bots["ore"] = 1
        # dfs
        max_nb_g = depth_first_search(32, resources, bots, bp)
        # compute sumprod
        ret *= max_nb_g
        print(">", max_nb_g)

    # 1 = 44
    # 2 = 46
    # 3 = >31
    # ans = 44*46* 31 = 62744

    return ret


# Test cases
##########


t1 = """Blueprint 1: Each ore robot costs 4 ore. \
    Each clay robot costs 2 ore. \
    Each obsidian robot costs 3 ore and 14 clay. \
    Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. \
    Each clay robot costs 3 ore. \
    Each obsidian robot costs 3 ore and 8 clay. \
    Each geode robot costs 3 ore and 12 obsidian."""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 33, True)
# sys.exit()
test_func(boom_part2, tt1, 3472, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d19.txt")

# part 1

r1 = run_func(boom_part1, puzzle_input, DBG=False)

# part 2

r2 = run_func(boom_part2, puzzle_input, DBG=False)

# print(f"Part 1 solution: {r1}")
print(f"Part 2 solution: {r2}")

sys.exit()

# PART 1 OK = 1177
# PART 2 OK = 62744
