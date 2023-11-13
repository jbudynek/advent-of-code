# coding: utf-8

# understood that each block is parametrized by 3 values
# and that you must work it backwards
# x and y are always zeroed so we don't need them in fact


# blocks are all like that:
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1  <-- this is our parameter p0
# add x 13 <-- this is our parameter p1
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 10 <-- this is our parameter p2
# mul y x
# add z y

# each block can be simplified to this python function


def step_forward(w, z, p0, p1, p2):

    z_div = z // p0
    if (z % 26 + p1) == w:
        z = z_div
    else:
        z = 26 * z_div + w + p2
    return (w, z)


# and can also be reversed
# got the solution from https://gist.github.com/jkseppan/1e36172ad4f924a8f86a920e4b1dc1b1


def step_backward(w, z, p0, p1, p2):
    zs = []
    x = z - w - p2
    if x % 26 == 0:
        zs.append(x // 26 * p0)
    if 0 <= w - p1 < 26:
        z0 = z * p0
        zs.append(w - p1 + z0)
    return zs


def lookup(ws):
    # extracted from input file, using google sheets!
    p0s = [
        1,
        1,
        1,
        1,
        26,
        26,
        1,
        26,
        1,
        26,
        1,
        26,
        26,
        26,
    ]
    p1s = [
        13,
        11,
        11,
        10,
        -14,
        -4,
        11,
        -3,
        12,
        -12,
        13,
        -12,
        -15,
        -12,
    ]
    p2s = [
        10,
        16,
        0,
        13,
        7,
        11,
        11,
        10,
        16,
        8,
        15,
        2,
        5,
        10,
    ]
    result = {}
    zs = {0}  # we want the last z to be 0
    for idx in range(14):
        p0 = p0s[13 - idx]
        p1 = p1s[13 - idx]
        p2 = p2s[13 - idx]
        newzs = set()
        for w in ws:
            for z in zs:
                z0s = step_backward(w, z, p0, p1, p2)
                for z0 in z0s:
                    newzs.add(z0)
                    if z not in result:
                        result[z] = []
                    result[z0] = [w] + result[z]
        zs = newzs
    return result


def boom_part1():

    ws = range(1, 10)  # iterate each input upwards
    result = lookup(ws)

    return "".join(str(digit) for digit in result[0])


def boom_part2():

    ws = range(9, 0, -1)  # iterate each input downwards
    result = lookup(ws)

    return "".join(str(digit) for digit in result[0])


ret = boom_part1()
print(ret)

ret = boom_part2()
print(ret)

# PART 1 OK = 98998519596997
# PART 2 OK = 31521119151421
