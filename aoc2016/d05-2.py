import hashlib
import sys

key = "wtnhxymk"

i = 1
k = 0
o = list("--------")
while True:

    test_me = key + str(i)
    md5_hex = str(hashlib.md5(test_me.encode("utf-8")).hexdigest())

    if md5_hex.startswith("00000"):
        print(str(i) + " " + md5_hex)
        pos = ord(md5_hex[5:6]) - ord("0")
        val = md5_hex[6:7]
        if pos >= 0 and pos < 8 and o[pos] == "-":
            o[pos] = val
            print("".join(o))
            k = k + 1
            if "-" not in o:
                print("".join(o))
                sys.exit()
    i = i + 1
