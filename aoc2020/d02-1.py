# coding: utf-8
import time
from collections import Counter


def is_valid(spec_and_password, DBG=True):
    # 1-3 a: abcde
    parts = spec_and_password.split(" ")
    letter = parts[1][0]
    password = parts[2]
    bounds = parts[0].split("-")
    low = int(bounds[0])
    high = int(bounds[1])
    counts = Counter(password)  # Counter({'l': 2, 'H': 1, 'e': 1, 'o': 1})
    if DBG:
        print(low, high, letter, password)
    return counts[letter] >= low and counts[letter] <= high


def boom(input_val, DBG=True):
    count = 0
    for sap in input_val:
        if is_valid(sap, DBG):
            count = count + 1
    return count


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


print(is_valid("1-3 a: abcde", True))

t1 = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
tt1 = t1.splitlines()
test(tt1, 2, True)
# sys.exit()

INPUT_FILE = "input-d02.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 1 = 396
