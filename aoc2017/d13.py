# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# A scanner of range r bounces back and forth with period 2*(r-1), and it is at
# the top of its layer at time t exactly when t % period == 0. The packet reaches
# layer `depth` at time delay + depth, so it is caught there iff
# (delay + depth) % period == 0. No simulation is needed.
# - Part 1: with delay 0, sum depth * range over the layers where we are caught.
# - Part 2: try delays 0, 1, 2, ... until no layer catches the packet.

ipt_test = """0: 3
1: 2
4: 4
6: 4"""

ipt_puzzle = open("input.txt").read().strip()


def parse(ipt):
    layers = []
    for line in ipt.splitlines():
        d, r = line.split(": ")
        layers.append((int(d), int(r)))
    return layers


def period(r):
    return max(2 * (r - 1), 1)


def severity(layers, delay=0):
    return sum(d * r for d, r in layers if (delay + d) % period(r) == 0)


def min_delay(layers):
    delay = 0
    while any((delay + d) % period(r) == 0 for d, r in layers):
        delay += 1
    return delay


# test
l_test = parse(ipt_test)
r_test1 = severity(l_test)
print(f"# Test part 1: {r_test1} (expected 24)")
r_test2 = min_delay(l_test)
print(f"# Test part 2: {r_test2} (expected 10)")
assert r_test1 == 24
assert r_test2 == 10

l = parse(ipt_puzzle)
r1 = severity(l)
r2 = min_delay(l)
print(f"# Part 1 solution: {r1}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1300
# Part 2 solution: 3870382
