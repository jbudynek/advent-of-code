# coding: utf-8
import time


def parse_input(iii, DBG=True):
    passports = []
    passport = {}
    for line in iii:
        if line == "":
            passports.append(passport)
            passport = {}
            continue
        kvs = line.split(" ")
        if DBG:
            print(kvs)
        for kv in kvs:
            parts = kv.split(":")
            passport[parts[0]] = parts[1]

    if len(passports) > 0:
        passports.append(passport)

    if DBG:
        print(passports)
    return passports


def is_valid(passport, DBG=True):
    mandatory = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    # optional = ["cid"]

    for m in mandatory:
        if m not in passport:
            return False

    return True


def boom(input_val, DBG=True):
    passports = parse_input(input_val, DBG)

    ret = 0
    for passport in passports:
        if is_valid(passport, DBG):
            ret = ret + 1

    return ret


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


t1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
tt1 = t1.splitlines()
test(tt1, 2, True)
# sys.exit()

INPUT_FILE = "input-d04.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 1 = 247
