# coding: utf-8
import re
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
            if DBG:
                print("incomplete")
            return False

    for m in mandatory:
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        byr = passport["byr"]
        if not (re.match(r"^[0-9]{4}$", byr) and int(byr) >= 1920 and int(byr) <= 2002):
            if DBG:
                print("byr", byr)
            return False
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        iyr = passport["iyr"]
        if not (re.match(r"^[0-9]{4}$", iyr) and int(iyr) >= 2010 and int(iyr) <= 2020):
            if DBG:
                print("iyr", iyr)
            return False
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        eyr = passport["eyr"]
        if not (re.match(r"^[0-9]{4}$", eyr) and int(eyr) >= 2020 and int(eyr) <= 2030):
            if DBG:
                print("eyr", eyr)
            return False
        # hgt (Height) - a number followed by either cm or in:
        hgt = passport["hgt"]
        if not (re.match(r"^[0-9]+cm$", hgt) or re.match(r"^[0-9]+in$", hgt)):
            if DBG:
                print("hgt", hgt)
            return False
        # If cm, the number must be at least 150 and at most 193.
        hgt_i = int(re.findall(r"\d+", hgt)[0])
        if re.match(r"^[0-9]+cm$", hgt) and not (hgt_i >= 150 and hgt_i <= 193):
            if DBG:
                print("hgt_i", hgt_i)
            return False
        # If in, the number must be at least 59 and at most 76.
        if re.match(r"^[0-9]+in$", hgt) and not (hgt_i >= 59 and hgt_i <= 76):
            if DBG:
                print("hgt_i", hgt_i)
            return False
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        hcl = passport["hcl"]
        if not (re.match(r"^#[0-9a-f]{6}$", hcl)):
            if DBG:
                print("hcl", hcl)
            return False
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        ecl = passport["ecl"]
        if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            if DBG:
                print("ecl", ecl)
            return False
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        pid = passport["pid"]
        if not (re.match(r"^[0-9]{9}$", pid)):
            if DBG:
                print("pid", pid)
            return False
    # cid (Country ID) - ignored, missing or not.

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


t1 = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
tt1 = t1.splitlines()
test(tt1, 4, True)
# sys.exit()

INPUT_FILE = "input-d04.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, False)
print(ret)

# part 2 = 145
