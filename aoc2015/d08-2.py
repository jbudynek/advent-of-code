# coding: utf-8
import re
import time


def boom(input_val, DBG=True):
    r_len = len(input_val)
    if DBG:
        print(input_val, r_len)

    input_val = re.sub(r"\\\\", "____", input_val, count=0)
    input_val = re.sub(r"\\\"", "____", input_val, count=0)
    input_val = re.sub(r"\\x[0-9a-fA-F][0-9a-fA-F]", "_____", input_val, count=0)

    r_len_2 = len(input_val) + 4
    if DBG:
        print(input_val, r_len_2)

    return (r_len, r_len_2)


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


tt1 = r'""'
test(tt1, (2, 6), False)
tt1 = r'"abc"'
test(tt1, (5, 9), False)
tt1 = r'"aaa\"aaa"'
test(tt1, (10, 16), False)
tt1 = r'"\x27"'
test(tt1, (6, 11), False)
# sys.exit()

INPUT_FILE = "input-d08.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ppc = 0
ppn = 0

for line in puzzle_input:
    (pp, nn) = boom(line, False)
    ppc += pp
    ppn += nn
print(ppn - ppc)

# 2046 OK
