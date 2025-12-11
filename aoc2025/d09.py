import shapely
from shapely.geometry import Polygon, box

ipt_test = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

ipt = ipt_puzzle

# ipt = ipt_test

polygon_list = []
for line in ipt:
    x, y = line.split(",")
    polygon_list.append((int(x), int(y)))

polygon_shp = Polygon(polygon_list)

nb_pts = len(polygon_list)
max_area1 = 0
max_area2 = 0

for i in range(nb_pts):
    for j in range(i + 1, nb_pts):
        z1 = polygon_list[j]
        z0 = polygon_list[i]
        area = int((abs(z1[1] - z0[1]) + 1) * (abs(z1[0] - z0[0]) + 1))
        max_area1 = max(area, max_area1)

        minx = min(z0[0], z1[0])
        maxx = max(z0[0], z1[0])
        miny = min(z0[1], z1[1])
        maxy = max(z0[1], z1[1])
        rect_shp = box(minx, miny, maxx, maxy)

        intersect_shp = polygon_shp.intersection(rect_shp)

        if shapely.equals(intersect_shp, rect_shp):
            max_area2 = max(area, max_area2)


print(f"# Part 1 solution: {max_area1}")
print(f"# Part 2 solution: {max_area2}")

# Part 1 solution: 4750297200
# Part 2 solution: 1578115935
