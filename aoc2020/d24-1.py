# coding: utf-8
from enum import Enum
from timeit import default_timer as timer


class Dir(Enum):
    e = 0
    se = 1
    sw = 2
    w = 3
    nw = 4
    ne = 5


DELTA = {
    Dir.e: complex(2, 0),
    Dir.se: complex(1, -1),
    Dir.sw: complex(-1, -1),
    Dir.w: complex(-2, 0),
    Dir.nw: complex(-1, 1),
    Dir.ne: complex(1, 1),
}

# black = 1
# white = 0


def parse_lines(input_val, DBG):
    lines = []

    for d in input_val:
        if d == "":
            continue
        line = []
        idx = 0
        while idx < len(d):
            if d[idx] == "e" or d[idx] == "w":
                dd = d[idx]
                line.append(Dir[dd])
                idx = idx + 1
            else:
                dd = Dir[d[idx] + d[idx + 1]]
                line.append(dd)
                idx = idx + 2
        lines.append(line)

    if DBG:
        print(lines)

    return lines


def follow_one_line(line, DBG):
    z = complex(0, 0)
    for d in line:
        z = z + DELTA[Dir(d)]
    if DBG:
        print("tile in ", z)
    return z


def follow_lines(lines, DBG=True):
    flipped_tiles = {}
    for line in lines:
        tile_to_flip = follow_one_line(line, DBG)
        if tile_to_flip not in flipped_tiles:
            flipped_tiles[tile_to_flip] = 0
        flipped_tiles[tile_to_flip] = (flipped_tiles[tile_to_flip] + 1) % 2

    number_black = sum(flipped_tiles.values())
    return number_black


################


def boom(input_val, DBG=True):
    lines = parse_lines(input_val, DBG)

    number_black = follow_lines(lines, DBG)

    return number_black


########################


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def test(cc=None, expected=None, DBG=False):
    t_start = timer()

    result = boom(cc, DBG)
    t_end = timer()

    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
    print_time(t_start, t_end)
    return flag


#######


t1 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

tt1 = t1.splitlines()
test(tt1, 10, True)
# sys.exit()

#########

INPUT_FILE = "input-d24.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

t_start = timer()

ret = boom(puzzle_input, DBG=False)

t_end = timer()
print_time(t_start, t_end)

print(ret)

# part 1 = 479
