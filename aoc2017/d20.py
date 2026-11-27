# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: in the long term, a particle is dominated by its acceleration;
#   rank particles by total absolute acceleration, then velocity and initial
#   position as stable tie-breakers.
# - Part 2: simulate all particles tick by tick, removing every particle in
#   each collision position so only collision-free particles remain.

import re

ipt_test = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""

ipt_test2 = """p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>"""

ipt_puzzle = open("input.txt").read().strip()


def parse(text):
    particles = []
    pattern = re.compile(r"<(-?\d+),(-?\d+),(-?\d+)>")
    for line in text.splitlines():
        matches = pattern.findall(line)
        p = tuple(map(int, matches[0]))
        v = tuple(map(int, matches[1]))
        a = tuple(map(int, matches[2]))
        particles.append([p, v, a])
    return particles


def manhattan(vector):
    return sum(abs(value) for value in vector)


def closest(text):
    particles = parse(text)
    return min(
        range(len(particles)),
        key=lambda i: (
            manhattan(particles[i][2]),
            manhattan(particles[i][1]),
            manhattan(particles[i][0]),
        ),
    )


def surviving(text, ticks=1000):
    particles = parse(text)
    for _ in range(ticks):
        for particle in particles:
            p, v, a = particle
            v = tuple(v_axis + a_axis for v_axis, a_axis in zip(v, a))
            p = tuple(p_axis + v_axis for p_axis, v_axis in zip(p, v))
            particle[0], particle[1] = p, v

        positions = {}
        for index, particle in enumerate(particles):
            positions.setdefault(particle[0], []).append(index)

        collided = {
            index
            for indices in positions.values()
            if len(indices) > 1
            for index in indices
        }
        particles = [
            particle
            for index, particle in enumerate(particles)
            if index not in collided
        ]

    return len(particles)


# test
r_test1 = closest(ipt_test)
print(f"# Test part 1: {r_test1} (expected 0)")
assert r_test1 == 0

r1 = closest(ipt_puzzle)
print(f"# Part 1 solution: {r1}")

# test part 2
r_test2 = surviving(ipt_test2)
print(f"# Test part 2: {r_test2} (expected 1)")
assert r_test2 == 1

r2 = surviving(ipt_puzzle)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 125
# Part 2 solution: 461
