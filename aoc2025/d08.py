ipt_test = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle
NN_MAX = 1000

# ipt = ipt_test
# NN_MAX = 10

all_boxes = {}
for r in ipt:
    x, y, z = r.split(",")
    x = int(x)
    y = int(y)
    z = int(z)
    all_boxes[(x, y, z)] = [x, y, z]

all_distances = {}
for box in all_boxes.keys():
    for box2 in all_boxes.keys():
        if box != box2:
            x1, y1, z1 = all_boxes[box]
            x2, y2, z2 = all_boxes[box2]
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            if box < box2:
                all_distances[(box, box2)] = dist

all_circuits = set()


def find_min_distance(all_distances):
    min_distance = float("inf")
    min_pair = None

    for pair, distance in all_distances.items():
        if distance < min_distance:
            min_distance = distance
            min_pair = pair

    return min_pair, min_distance


nn = 0

res1, res2 = 0, 0

box2circuit = {}
for box in all_boxes.keys():
    box2circuit[box] = set()
    box2circuit[box].add(box)

while True:
    boxes, dist = find_min_distance(all_distances)
    del all_distances[boxes]
    box2circuit[boxes[0]].add(boxes[1])
    for b in box2circuit[boxes[0]]:
        box2circuit[b].update(box2circuit[boxes[0]])
    for b in box2circuit[boxes[1]]:
        box2circuit[b].update(box2circuit[boxes[1]])

    all_circuits = set()
    for k, v in box2circuit.items():
        all_circuits.add(tuple(sorted(v)))
    if len(all_circuits) == 1:
        res2 = boxes[0][0] * boxes[1][0]
        break

    nn += 1
    if nn == NN_MAX:
        longest_circuits = sorted(all_circuits, key=len, reverse=True)[:3]
        res1 = 1
        for i in range(len(longest_circuits)):
            res1 *= len(longest_circuits[i])


print(f"# Part 1 solution: {res1}")
print(f"# Part 2 solution: {res2}")

# works but ugly and slow!!!

# Part 1 solution: 96672
# # Part 2 solution: 22517595
