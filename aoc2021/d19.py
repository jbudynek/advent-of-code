# coding: utf-8
from collections import Counter, defaultdict
import copy
import re
from timeit import default_timer as timer

import numpy as np

# Main function
##########


class Scanner:
    pass


def parse_scanners(input_val):
    cur_scan = Scanner()
    idx = 0
    ret = []
    while idx < len(input_val):
        ll = input_val[idx]
        if ll == '':
            idx += 1
            continue
        elif ll[1] == '-' and ll[0] == '-':
            cur_scan = Scanner()
            cur_scan.position = (0, 0, 0)
            cur_scan.rot_dir = (0, 0)
            cur_scan.beacons = []
            cur_scan.id = int(re.findall(r'-?\d+', ll)[0])
            ret.append(cur_scan)
        else:
            xyz = np.asarray(re.findall(r'-?\d+', ll), dtype=int)
            cur_scan.beacons.append((xyz[0], xyz[1], xyz[2]))
        idx += 1

    return ret


def get_all_rot_dir():
    # first part = permutations of xyz
    # second pars = +/- signs in front of x y z
    # 6*8 = 48 possibilities, there must be repetitions

    return [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),

        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),

        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),

        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),

        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 7),

        (5, 0),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (5, 6),
        (5, 7),
    ]


def apply_rot_dir(scan, rot_dir):
    # first part = permutations of xyz
    # second pars = +/- signs in front of x y z
    # 6*8 = 48 possibilities, there must be repetitions
    scan.rot_dir = rot_dir

    shift = rot_dir[0]
    minus = rot_dir[1]

    nb_b = len(scan.beacons)
    idx = 0
    while idx < nb_b:
        b = scan.beacons[idx]

        if shift == 0:
            scan.beacons[idx] = b[0], b[1], b[2]
        elif shift == 1:
            scan.beacons[idx] = b[0], b[2], b[1]
        elif shift == 2:
            scan.beacons[idx] = b[1], b[0], b[2]
        elif shift == 3:
            scan.beacons[idx] = b[1], b[2], b[0]
        elif shift == 4:
            scan.beacons[idx] = b[2], b[0], b[1]
        elif shift == 5:
            scan.beacons[idx] = b[2], b[1], b[0]

        b = scan.beacons[idx]

        if minus == 0:
            scan.beacons[idx] = b[0], b[1], b[2]
        elif minus == 1:
            scan.beacons[idx] = b[0], b[1], -b[2]
        elif minus == 2:
            scan.beacons[idx] = b[0], -b[1], b[2]
        elif minus == 3:
            scan.beacons[idx] = b[0], -b[1], -b[2]
        elif minus == 4:
            scan.beacons[idx] = -b[0], b[1], b[2]
        elif minus == 5:
            scan.beacons[idx] = -b[0], b[1], -b[2]
        elif minus == 6:
            scan.beacons[idx] = -b[0], -b[1], b[2]
        elif minus == 7:
            scan.beacons[idx] = -b[0], -b[1], -b[2]
        idx += 1

    return scan


def match(ks, us):
    # performance is quite bad, there must be a better way to see if it matches, possibly with convolutions?

    nkb = len(ks.beacons)
    nub = len(us.beacons)
    s_world = defaultdict(int)
    for b in ks.beacons:
        xyz = (ks.position[0]+b[0], ks.position[1]+b[1], ks.position[2]+b[2])
        s_world[xyz] += 1

    for i_k in range(nkb):
        for i_u in range(i_k, nub):
            k_xyz = (ks.beacons[i_k][0] + ks.position[0], ks.beacons[i_k]
                     [1] + ks.position[1], ks.beacons[i_k][2] + ks.position[2])
            u_xyz = (us.beacons[i_u][0] + us.position[0], us.beacons[i_u]
                     [1] + us.position[1], us.beacons[i_u][2] + us.position[2])

            delta = (u_xyz[0]-k_xyz[0], u_xyz[1]-k_xyz[1], u_xyz[2]-k_xyz[2])

            world = copy.deepcopy(s_world)

            for bus in us.beacons:
                u_xyz = (us.position[0]+bus[0] - delta[0], us.position[1] +
                         bus[1] - delta[1], us.position[2]+bus[2] - delta[2])
                world[u_xyz] += 1

            c2 = Counter(world.values())[2]
            if c2 >= 12:
                return True, (-delta[0], -delta[1], -delta[2])

    return False, (0, 0, 0)


def compute_known_scanners(input_val):

    # struct to hold scanner id, position, rotation, orientation, and what it detects

    # parse and populate scanner 0 - this is what will not move
    # parse and populate scanners 1..n - we don't know position, rotation, orientation
    all_scanners = parse_scanners(input_val)
    #all_scanners = all_scanners[0:2]+[all_scanners[4]] # for "unit tests"

    # put scanner 0 in known_scanners
    # put scanners 1..n in unknown_scanners

    known_scanners = []
    known_scanners.append(copy.deepcopy(all_scanners[0]))
    unknown_scanners = []
    unknown_scanners.extend(all_scanners[1:])

    # while unknown scanners is not empty
    # current scanner = first in the queue
    # loop on (rotation, orientation) with a sort of permutation enumerator
    # apply transformation
    # loop on known scanners
    # see if it matches on more than 12 points
    # if yes, add current scanner to known scanners list

    while len(unknown_scanners) > 0:
        current_scanner = unknown_scanners[0]
        del unknown_scanners[0]
        rot_dirs = get_all_rot_dir()
        found = False
        for cur_rot_dir in rot_dirs:
            if found:
                continue
            test_scanner = apply_rot_dir(
                copy.deepcopy(current_scanner), cur_rot_dir)
            for ks in known_scanners:  # TODO SWITCH WITH OTHER LOOP
                if found:
                    continue
                mm, xyz = match(ks, test_scanner)
                if mm:
                    found = True
                    test_scanner.position = xyz
                    print("intersection ", ks.id, test_scanner.id,
                          xyz, "--", len(unknown_scanners), "left")
        if not found:
            unknown_scanners.append(current_scanner)
        else:
            known_scanners.append(copy.deepcopy(test_scanner))

    return known_scanners


def boom_all(input_val):

    # both parts in the same function

    known_scanners = compute_known_scanners(input_val)

    all_beacons = {}
    for ks in known_scanners:
        for b in ks.beacons:
            bb = (b[0]+ks.position[0], b[1] +
                  ks.position[1], b[2]+ks.position[2])
            if bb not in all_beacons:
                all_beacons[bb] = 1

    ret1 = len(all_beacons)

    max_manhattan = 0
    nks = len(known_scanners)
    for i_ks in range(nks):
        for j_ks in range(i_ks+1, nks):
            pos1 = known_scanners[i_ks].position
            pos2 = known_scanners[j_ks].position
            manhattan = abs(pos2[0]-pos1[0]) + \
                abs(pos2[1]-pos1[1])+abs(pos2[2]-pos1[2])
            max_manhattan = max(max_manhattan, manhattan)

    ret2 = max_manhattan
    return ret1, ret2


def boom_part1(input_val, DBG=True):
    ret1, _ = boom_all(input_val)
    return ret1


def boom_part2(input_val, DBG=True):
    _, ret2 = boom_all(input_val)
    return ret2


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)

# Test cases
##########


tt1 = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
tt1 = tt1.splitlines()
test_part1(tt1, 79, True)
test_part2(tt1, 3621, True)

# Real data
##########

INPUT_FILE = "input-d19.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1 + 2

t_start = timer()
ret = boom_all(puzzle_input)
t_end = timer()
print_time(t_start, t_end)
print(ret)


# PART 1 OK = 436 - runtime 43 mins :/
# PART 2 OK = 10918 - runtime 43 mins :/
