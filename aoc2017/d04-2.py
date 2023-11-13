# coding: utf-8
import time
from collections import Counter


def function(ii, DBG=True):

    words_raw = ii.split()
    words = []
    # x = np.array(numbers)
    for ww in words_raw:
        words.append("".join(sorted(ww)))
    c = Counter(words)
    most = c.most_common(1)
    if DBG:
        print(most)
    count = most[0][1]
    return count == 1


def test(cc=None, expected=None, DBG=False):

    start_millis = int(round(time.time() * 1000))
    result = str(function(cc, DBG))
    stop_millis = int(round(time.time() * 1000))

    expected = str(expected)
    flag = result == expected
    print(
        "*** " + str(cc) + " *** -> Result = " + str(result),
        " -> success = " + str(flag) + " -> expected " + expected,
    )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )


t1 = "abcde fghij"
test(t1, True, True)  #

t2 = "abcde xyz ecdab"
test(t2, False, True)  #

t3 = "a ab abc abd abf abj"
test(t3, True, True)  #

t4 = "iiii oiii ooii oooi oooo"
test(t4, True, True)  #

t5 = "oiii ioii iioi iiio"
test(t5, False, True)  #

INPUT_FILE = "input-d04.txt"

f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()


nn = 0
kk = 0
for pp in puzzle_input:
    result = function(pp, False)
    nn = nn + result
    kk = kk + 1
    # if (kk==10):break
print(nn)

#################
