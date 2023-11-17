# coding: utf-8

import time

import networkx as nx

# fmt: off
puzzle_input = [1, 330, 331, 332, 109, 3080, 1101, 0, 1182, 15, 1101, 0, 1403, 24, 1001, 0, 0, 570, 1006, 570, 36, 1002, 571, 1, 0, 1001, 570, -1, 570, 1001, 24, 1, 24, 1105, 1, 18, 1008, 571, 0, 571, 1001, 15, 1, 15, 1008, 15, 1403, 570, 1006, 570, 14, 21101, 58, 0, 0, 1105, 1, 786, 1006, 332, 62, 99, 21102, 333, 1, 1, 21101, 0, 73, 0, 1105, 1, 579, 1102, 0, 1, 572, 1101, 0, 0, 573, 3, 574, 101, 1, 573, 573, 1007, 574, 65, 570, 1005, 570, 151, 107, 67, 574, 570, 1005, 570, 151, 1001, 574, -64, 574, 1002, 574, -1, 574, 1001, 572, 1, 572, 1007, 572, 11, 570, 1006, 570, 165, 101, 1182, 572, 127, 101, 0, 574, 0, 3, 574, 101, 1, 573, 573, 1008, 574, 10, 570, 1005, 570, 189, 1008, 574, 44, 570, 1006, 570, 158, 1106, 0, 81, 21102, 1, 340, 1, 1105, 1, 177, 21102, 477, 1, 1, 1105, 1, 177, 21102, 1, 514, 1, 21102, 1, 176, 0, 1106, 0, 579, 99, 21101, 184, 0, 0, 1105, 1, 579, 4, 574, 104, 10, 99, 1007, 573, 22, 570, 1006, 570, 165, 1002, 572, 1, 1182, 21101, 0, 375, 1, 21102, 211, 1, 0, 1105, 1, 579, 21101, 1182, 11, 1, 21102, 1, 222, 0, 1106, 0, 979, 21101, 0, 388, 1, 21102, 233, 1, 0, 1105, 1, 579, 21101, 1182, 22, 1, 21101, 244, 0, 0, 1105, 1, 979, 21101, 0, 401, 1, 21101, 255, 0, 0, 1106, 0, 579, 21101, 1182, 33, 1, 21101, 266, 0, 0, 1106, 0, 979, 21101, 0, 414, 1, 21102, 1, 277, 0, 1105, 1, 579, 3, 575, 1008, 575, 89, 570, 1008, 575, 121, 575, 1, 575, 570, 575, 3, 574, 1008, 574, 10, 570, 1006, 570, 291, 104, 10, 21101, 1182, 0, 1, 21101, 313, 0, 0, 1105, 1, 622, 1005, 575, 327, 1101, 1, 0, 575, 21101, 327, 0, 0, 1106, 0, 786, 4, 438, 99, 0, 1, 1, 6, 77, 97, 105, 110, 58, 10, 33, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 110, 97, 109, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 0, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 65, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 66, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 67, 58, 10, 23, 67, 111, 110, 116, 105, 110, 117, 111, 117, 115, 32, 118, 105, 100, 101, 111, 32, 102, 101, 101, 100, 63, 10, 0, 37, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 82, 44, 32, 76, 44, 32, 111, 114, 32, 100, 105, 115, 116, 97, 110, 99, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 36, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 99, 111, 109, 109, 97, 32, 111, 114, 32, 110, 101, 119, 108, 105, 110, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 43, 10, 68, 101, 102, 105, 110, 105, 116, 105, 111, 110, 115, 32, 109, 97, 121, 32, 98, 101, 32, 97, 116, 32, 109, 111, 115, 116, 32, 50, 48, 32, 99, 104, 97, 114, 97, 99, 116, 101, 114, 115, 33, 10, 94, 62, 118, 60, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 20, 26, 0, 109, 4, 1202, -3, 1, 587, 20102, 1, 0, -1, 22101, 1, -3, -3, 21101, 0, 0, -2, 2208, -2, -1, 570, 1005, 570, 617, 2201, -3, -2, 609, 4, 0, 21201, -2, 1, -2, 1106, 0, 597, 109, -4, 2106, 0, 0, 109, 5, 1202, -4, 1, 630, 20101, 0, 0, -2, 22101, 1, -4, -4, 21102, 0, 1, -3, 2208, -3, -2, 570, 1005, 570, 781, 2201, -4, -3, 653, 20102, 1, 0, -1, 1208, -1, -4, 570, 1005, 570, 709, 1208, -1, -5, 570, 1005, 570, 734, 1207, -1, 0, 570, 1005, 570, 759, 1206, -1, 774, 1001, 578, 562, 684, 1, 0, 576, 576, 1001, 578, 566, 692, 1, 0, 577, 577, 21101, 0, 702, 0, 1105, 1, 786, 21201, -1, -1, -1, 1106, 0, 676, 1001, 578, 1, 578, 1008, 578, 4, 570, 1006, 570, 724, 1001, 578, -4, 578, 21102, 1, 731, 0, 1106, 0, 786, 1105, 1, 774, 1001, 578, -1, 578, 1008, 578, -1, 570, 1006, 570, 749, 1001, 578, 4, 578, 21101, 756, 0, 0, 1105, 1, 786, 1106, 0, 774, 21202, -1, -11, 1, 22101, 1182, 1, 1, 21101, 774, 0, 0, 1105, 1, 622, 21201, -3, 1, -3, 1106, 0, 640, 109, -5, 2105, 1, 0, 109, 7, 1005, 575, 802, 20101, 0, 576, -6, 21002, 577, 1, -5, 1106, 0, 814, 21102, 0, 1, -1, 21101, 0, 0, -5, 21101, 0, 0, -6, 20208, -6, 576, -2, 208, -5, 577, 570, 22002, 570, -2, -2, 21202, -5, 43, -3, 22201, -6, -3, -3, 22101, 1403, -3, -3, 2102, 1, -3, 843, 1005, 0, 863, 21202, -2, 42, -4, 22101, 46, -4, -4, 1206, -2, 924, 21101, 0, 1, -1, 1106, 0, 924, 1205, -2, 873, 21101, 35, 0, -4, 1106, 0, 924, 1201, -3, 0, 878, 1008, 0, 1, 570, 1006, 570, 916, 1001, 374, 1, 374, 1201, -3, 0, 895, 1101, 2, 0, 0, 1201, -3, 0, 902, 1001, 438, 0, 438, 2202, -6, -5, 570, 1, 570, 374, 570, 1, 570, 438, 438, 1001, 578, 558, 922, 20102, 1, 0, -4, 1006, 575, 959, 204, -4, 22101, 1, -6, -6, 1208, -6, 43, 570, 1006, 570, 814, 104, 10, 22101, 1, -5, -5, 1208, -5, 39, 570, 1006, 570, 810, 104, 10, 1206, -1, 974, 99, 1206, -1, 974, 1101, 0, 1, 575, 21101, 0, 973, 0, 1105, 1, 786, 99, 109, -7, 2105, 1, 0, 109, 6, 21101, 0, 0, -4, 21101, 0, 0, -3, 203, -2, 22101, 1, -3, -3, 21208, -2, 82, -1, 1205, -1, 1030, 21208, -2, 76, -1, 1205, -1, 1037, 21207, -2, 48, -1, 1205, -1, 1124, 22107, 57, -2, -1, 1205, -1, 1124, 21201, -2, -48, -2, 1106, 0, 1041, 21102, 1, -4, -2, 1106, 0, 1041, 21102, 1, -5, -2, 21201, -4, 1, -4, 21207, -4, 11, -1, 1206, -1, 1138, 2201, -5, -4, 1059, 1201, -2, 0, 0, 203, -2, 22101, 1, -3, -3, 21207, -2, 48, -1, 1205, -1, 1107, 22107, 57, -2, -1, 1205, -1, 1107, 21201, -2, -48, -2, 2201, -5, -4, 1090, 20102, 10, 0, -1, 22201, -2, -1, -2, 2201, -5, -4, 1103, 2101, 0, -2, 0, 1106, 0, 1060, 21208, -2, 10, -1, 1205, -1, 1162, 21208, -2, 44, -1, 1206, -1, 1131, 1105, 1, 989, 21101, 0, 439, 1, 1106, 0, 1150, 21102, 1, 477, 1, 1106, 0, 1150, 21101, 514, 0, 1, 21101, 1149, 0, 0, 1106, 0, 579, 99, 21101, 1157, 0, 0, 1105, 1, 579, 204, -2, 104, 10, 99, 21207, -3, 22, -1, 1206, -1, 1138, 1201, -5, 0, 1176, 2101, 0, -4, 0, 109, -6, 2105, 1, 0, 28, 5, 38, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 34, 9, 34, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 34, 9, 34, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 34, 5, 3, 5, 30, 1, 11, 1, 30, 1, 11, 1, 30, 1, 11, 1, 22, 9, 11, 5, 18, 1, 23, 1, 18, 1, 23, 1, 18, 1, 23, 1, 10, 7, 1, 1, 19, 9, 6, 1, 5, 1, 1, 1, 19, 1, 3, 1, 3, 1, 6, 1, 5, 1, 1, 5, 15, 1, 3, 1, 3, 1, 6, 1, 5, 1, 5, 1, 15, 1, 3, 1, 3, 1, 6, 11, 1, 1, 1, 7, 3, 5, 3, 11, 6, 1, 3, 1, 1, 1, 1, 1, 9, 1, 11, 1, 5, 1, 6, 1, 1, 9, 7, 1, 11, 1, 5, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 11, 1, 5, 1, 6, 9, 1, 9, 11, 7, 8, 1, 1, 1, 1, 1, 3, 1, 30, 9, 3, 1, 30, 1, 3, 1, 1, 1, 5, 1, 30, 1, 3, 1, 1, 7, 30, 1, 3, 1, 38, 1, 3, 1, 38, 1, 3, 1, 38, 5, 34, ] # noqa
# fmt: on


CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"


def delete_last_lines(n=1):
    for _ in range(n):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)


#        sys.stdout.write(CURSOR_UP_ONE)
#        sys.stdout.write(ERASE_LINE)


def print_field(xyids, DBG=True):
    coords = xyids.keys()
    if DBG:
        print(xyids)
    x_min = min(coords, key=lambda t: t[0])[0] - 1
    x_max = max(coords, key=lambda t: t[0])[0] + 1
    y_min = min(coords, key=lambda t: t[1])[1] - 1
    y_max = max(coords, key=lambda t: t[1])[1] + 1

    if DBG:
        print(x_min, x_max, y_min, y_max)

    for yy in range(y_min, y_max + 1):
        ss = ""
        for xx in range(x_min, x_max + 1):
            if (xx, yy) in xyids:
                ss += str(xyids[(xx, yy)])
            else:
                ss += " "
        print(ss)

    # delete_last_lines(y_max-y_min)


# OPCODE INT MACHINE


def to_ascii(ccc):
    ret = []
    for c in ccc:
        ret.append(ord(c))
    ret.append(10)
    return ret


def from_ascii(aaa):
    ret = ""
    for a in aaa:
        if a < 256:
            ret += chr(a)
        else:
            ret += str(a)
    return ret


def decode(c):  # returns mode_a,mode_b,mode_c,opcode
    code_5 = "{:05d}".format(c)
    return (
        int(code_5[0]),
        int(code_5[1]),
        int(code_5[2]),
        10 * int(code_5[3]) + int(code_5[4]),
    )


def code_to_dictcode(code):
    dictcode = {i: code[i] for i in range(0, len(code))}
    return dictcode


def get_dictcode(i, dictcode):  # handle negative?
    if i not in dictcode:
        return 0
    return dictcode[i]


def set_dictcode(i, value, dictcode):  # handle negative?
    dictcode[i] = value


# if one_output=True --> returns OUTPUT - array of outputs
# else
# returns output,dictcode,i,input_signals,input_index,relative_base
def opcode_machine(
    dictcode, i, input_signals, input_index, relative_base, one_output=True, DBG=False
):

    code_i = get_dictcode(i, dictcode)
    mode_a, mode_b, mode_c, opcode = decode(code_i)

    output = []

    while True:

        if DBG:
            print(code_i, mode_a, mode_b, mode_c, opcode)

        if mode_c == 0:  # position mode
            i1 = get_dictcode(i + 1, dictcode)
        elif mode_c == 1:  # immediate mode
            i1 = i + 1
        elif mode_c == 2:  # relative mode
            i1 = get_dictcode(i + 1, dictcode) + relative_base

        if mode_b == 0:  # position mode
            i2 = get_dictcode(i + 2, dictcode)
        elif mode_b == 1:  # immediate mode
            i2 = i + 2
        elif mode_b == 2:  # relative mode
            i2 = get_dictcode(i + 2, dictcode) + relative_base

        if mode_a == 0:  # position mode
            i3 = get_dictcode(i + 3, dictcode)
        elif mode_a == 1:  # immediate mode
            i3 = i + 3
        elif mode_a == 2:  # relative mode
            i3 = get_dictcode(i + 3, dictcode) + relative_base

        code_i1 = get_dictcode(i1, dictcode)
        code_i2 = get_dictcode(i2, dictcode)
        _ = get_dictcode(i3, dictcode)

        if opcode == 99:
            if DBG:
                print("HALT")
            if one_output:
                return ("HALT", dictcode, i, input_signals, input_index, relative_base)
            else:
                return output
        elif opcode == 1:  # addition
            set_dictcode(i3, code_i1 + code_i2, dictcode)
            i = i + 4
        elif opcode == 2:  # multiplication
            set_dictcode(i3, code_i1 * code_i2, dictcode)
            i = i + 4
        elif opcode == 3:  # input
            set_dictcode(i1, input_signals[input_index], dictcode)
            if input_index < len(input_signals) - 1:
                input_index += 1
            else:
                input_index += 0
                # print("no more input signals")
            i = i + 2
        elif opcode == 4:  # output
            output = output + [code_i1]
            if DBG:
                print(code_i1)
            i = i + 2
            if one_output:
                return (output, dictcode, i, input_signals, input_index, relative_base)
        elif opcode == 5:  # jump-if-true
            if code_i1 != 0:
                i = code_i2
            else:
                i = i + 3
        elif opcode == 6:  # jump-if-false
            if code_i1 == 0:
                i = code_i2
            else:
                i = i + 3
        elif opcode == 7:  # less than
            if code_i1 < code_i2:
                set_dictcode(i3, 1, dictcode)
            else:
                set_dictcode(i3, 0, dictcode)
            i = i + 4
        elif opcode == 8:  # equals
            if code_i1 == code_i2:
                set_dictcode(i3, 1, dictcode)
            else:
                set_dictcode(i3, 0, dictcode)
            i = i + 4
        elif opcode == 9:  # relative base update
            relative_base += code_i1
            i = i + 2

        if DBG:
            print("i", i)
            print("relative_base", relative_base)
            print("dictcode", dictcode)
        code_i = get_dictcode(i, dictcode)
        mode_a, mode_b, mode_c, opcode = decode(code_i)

    # we never get there
    return "NEVER"


def connect(xx, yy, kkk, g_all, field):
    k_c = (xx, yy)
    if k_c in field:
        kkc = (xx, yy, field[k_c])
        g_all.add_node(kkc)
        g_all.add_edge(kkc, kkk)


def parse_opcode(cc, DBG=True):

    dictcode = code_to_dictcode(cc)
    i = 0
    input_signals = []
    input_index = 0
    relative_base = 0

    output = opcode_machine(
        dictcode,
        i,
        input_signals,
        input_index,
        relative_base,
        one_output=False,
        DBG=False,
    )

    fff = from_ascii(output)
    if DBG:
        print(fff)
    return fff


def create_world(fff, DBG=True):
    field = {}
    g_all = nx.Graph()
    entry = ""
    x = -1
    y = -1

    for line in fff.splitlines():
        y += 1
        x = -1
        for c in line:
            x += 1
            if c != ".":
                field[(x, y)] = c

    if DBG:
        print(field)
    if DBG:
        print_field(field)

    for k in field.keys():
        (x, y) = k
        kkk = (x, y, field[k])
        # connect
        # left
        connect(x - 1, y, kkk, g_all, field)
        # right
        connect(x + 1, y, kkk, g_all, field)
        # up
        connect(x, y - 1, kkk, g_all, field)
        # down
        connect(x, y + 1, kkk, g_all, field)
        #
        if field[k] == "^":
            entry = kkk

    if DBG:
        print("***FINAL GRAPH")
    if DBG:
        print("nodes", len(g_all.nodes), list(g_all.nodes))
    if DBG:
        print("edges", len(g_all.edges), list(g_all.edges))
    if DBG:
        print("#nodes", len(g_all.nodes))
    if DBG:
        print("#edges", len(g_all.edges))
    if DBG:
        print("entry", entry)
    if DBG:
        print("***END FINAL GRAPH")
    if DBG:
        pass
        # nx.draw(g, with_labels=True, font_weight='bold')
        # nx.draw_shell(g, with_labels=True, font_weight='bold')
        # nx.draw_circular(g, with_labels=True, font_weight='bold')
        # nx.draw_kamada_kawai(g_all, with_labels=True, font_weight='bold')
        # nx.draw_random(g, with_labels=True, font_weight='bold')
        # nx.draw_spectral(g, with_labels=True, font_weight='bold')
        # nx.draw_spring(g_all, with_labels=True, font_weight='bold')

    return g_all, field, entry


def function(ccc, field, entry, DBG=False):

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    # turn left = dir +1

    out = ""
    count = 0
    (curx, cury) = (entry[0], entry[1])
    cur_dir = 2

    idx = 0
    while 1:
        if DBG:
            print(out)
        idx += 1
        if idx >= 1000:
            break
        (x1, y1) = (curx + directions[cur_dir][0], cury + directions[cur_dir][1])
        if (x1, y1) in field:
            count = count + 1
            (curx, cury) = (x1, y1)
        else:
            if count > 0:
                out += str(count) + ","
            # test turn right
            new_dir = (cur_dir - 1) % 4
            (xt, yt) = (curx + directions[new_dir][0], cury + directions[new_dir][1])
            if (xt, yt) in field:
                cur_dir = new_dir
                count = 0
                out += "L,"
                continue
            # test turn left
            new_dir = (cur_dir + 1) % 4
            (xt, yt) = (curx + directions[new_dir][0], cury + directions[new_dir][1])
            if (xt, yt) in field:
                cur_dir = new_dir
                count = 0
                out += "R,"
                continue
            # break
            break

    out = out[: len(out) - 1]
    return out


def test(cc=None, opcode=True, expected=None, DBG=True):

    start_millis = int(round(time.time() * 1000))
    if opcode:
        ff = parse_opcode(cc, DBG)
        cc = ff
    else:
        ff = cc
    g_all, field, entry = create_world(ff, DBG)
    result = function(g_all, field, entry, DBG)
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "***" + str(cc) + " -> " + str(result), " -> " + str(flag) + " vs " + expected
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


t1 = """#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""


test(
    t1,
    opcode=False,
    expected="R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2",
    DBG=False,
)

test(puzzle_input, opcode=True, expected=0, DBG=False)


def test2(cc=None, opcode=True, input_commands=[], expected=None, DBG=True):

    start_millis = int(round(time.time() * 1000))
    cc[0] = 2

    dictcode = code_to_dictcode(cc)
    i = 0
    command = input_commands.pop(0)
    print("***", command)
    input_signals = to_ascii(command)
    input_index = 0
    relative_base = 0

    while 1:
        output = []
        answer = []

        while 1:
            (
                output,
                dictcode,
                i,
                input_signals,
                input_index,
                relative_base,
            ) = opcode_machine(
                dictcode,
                i,
                input_signals,
                input_index,
                relative_base,
                one_output=True,
                DBG=False,
            )

            # print(output)
            # print(from_ascii(output))
            if output == []:
                break
            if output == "HALT":
                # answer.append(output[0][1])
                print("HALT")
                break
            else:
                answer.append(output[0])

        print("ANSWER", from_ascii(answer))
        if output == "HALT":
            print("GAME OVER")
            break

        if len(input_commands) > 0:
            command = input_commands.pop(0)
            print("**", command)
            input_signals = to_ascii(command)
        else:
            aa = input()
            input_signals = to_ascii(aa)
        input_index = 0
        # print(input_signals)

    result = output

    ######

    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "***" + str(input_commands) + " -> " + str(result),
        " -> " + str(flag) + " vs " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


input_commands = [
    "A,C,A,B,C,B,C,B,A,C"
    + chr(10)
    + "L,6,L,4,R,8"
    + chr(10)
    + "L,4,R,4,L,4,R,8"
    + chr(10)
    + "R,8,L,6,L,4,L,10,R,8"
    + chr(10)
    + "n"
]

test2(puzzle_input, opcode=True, input_commands=input_commands, expected=0, DBG=False)


# L,6,L,4,R,8,R,8,L,6,L,4,L,10,R,8,L,6,L,4,R,8,L,4,R,4,L,4,R,8,R,8,L,6,L,4,L,10,R,8,L,4,R,4,L,4,R,8,R,8,L,6,L,4,L,10,R,8,L,4,R,4,L,4,R,8,L,6,L,4,R,8,R,8,L,6,L,4,L,10,R,8

# A = L,6,L,4,R,8
# B = L,4,R,4,L,4,R,8
# C = R,8,L,6,L,4,L,10,R,8

# A,C,A,B,C,B,C,B,A,C
