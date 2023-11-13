# coding: utf-8


def parse_line(ll):
    ii = ll.split(" ")
    return (ii[0], int(ii[1]))


def boom(input_val, DBG=True):

    x = 0
    y = 0
    aim = 0

    for ll in input_val:
        (cmd, val) = parse_line(ll)
        if cmd == "forward":
            x += val
            y += aim * val
        elif cmd == "up":
            aim -= val
        elif cmd == "down":
            aim += val

    return x * y


#############


INPUT_FILE = "input-d02.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=False)

print(ret)

# PART 2 - 2101031224 OK
