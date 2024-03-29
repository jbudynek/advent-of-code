# coding: utf-8

# In[1]:


import numpy as np

# fmt: off
puzzle_input = [109,2050,21102,1,966,1,21102,13,1,0,1106,0,1378,21101,20,0,0,1106,0,1337,21101,27,0,0,1106,0,1279,1208,1,65,748,1005,748,73,1208,1,79,748,1005,748,110,1208,1,78,748,1005,748,132,1208,1,87,748,1005,748,169,1208,1,82,748,1005,748,239,21102,1,1041,1,21102,73,1,0,1106,0,1421,21102,78,1,1,21101,1041,0,2,21101,88,0,0,1105,1,1301,21102,1,68,1,21101,1041,0,2,21102,103,1,0,1105,1,1301,1101,1,0,750,1106,0,298,21102,82,1,1,21101,0,1041,2,21102,125,1,0,1106,0,1301,1101,2,0,750,1106,0,298,21101,0,79,1,21102,1041,1,2,21101,147,0,0,1106,0,1301,21102,1,84,1,21101,1041,0,2,21101,0,162,0,1105,1,1301,1101,3,0,750,1106,0,298,21101,65,0,1,21101,1041,0,2,21102,184,1,0,1105,1,1301,21101,0,76,1,21101,1041,0,2,21102,199,1,0,1105,1,1301,21101,75,0,1,21101,1041,0,2,21101,0,214,0,1105,1,1301,21102,1,221,0,1105,1,1337,21101,0,10,1,21102,1041,1,2,21101,236,0,0,1105,1,1301,1106,0,553,21101,85,0,1,21102,1041,1,2,21101,254,0,0,1106,0,1301,21102,1,78,1,21101,0,1041,2,21101,269,0,0,1106,0,1301,21101,276,0,0,1105,1,1337,21101,0,10,1,21101,1041,0,2,21101,0,291,0,1105,1,1301,1102,1,1,755,1105,1,553,21101,0,32,1,21102,1041,1,2,21101,313,0,0,1106,0,1301,21101,0,320,0,1105,1,1337,21101,327,0,0,1105,1,1279,1202,1,1,749,21101,0,65,2,21102,1,73,3,21102,346,1,0,1105,1,1889,1206,1,367,1007,749,69,748,1005,748,360,1102,1,1,756,1001,749,-64,751,1105,1,406,1008,749,74,748,1006,748,381,1102,1,-1,751,1105,1,406,1008,749,84,748,1006,748,395,1102,1,-2,751,1106,0,406,21102,1100,1,1,21101,406,0,0,1105,1,1421,21102,1,32,1,21101,0,1100,2,21102,421,1,0,1105,1,1301,21102,428,1,0,1105,1,1337,21101,435,0,0,1106,0,1279,1202,1,1,749,1008,749,74,748,1006,748,453,1101,-1,0,752,1106,0,478,1008,749,84,748,1006,748,467,1101,-2,0,752,1106,0,478,21101,0,1168,1,21102,1,478,0,1105,1,1421,21101,0,485,0,1106,0,1337,21101,0,10,1,21102,1168,1,2,21102,500,1,0,1105,1,1301,1007,920,15,748,1005,748,518,21102,1209,1,1,21102,1,518,0,1106,0,1421,1002,920,3,529,1001,529,921,529,102,1,750,0,1001,529,1,537,101,0,751,0,1001,537,1,545,1001,752,0,0,1001,920,1,920,1106,0,13,1005,755,577,1006,756,570,21102,1,1100,1,21101,570,0,0,1105,1,1421,21102,1,987,1,1106,0,581,21102,1,1001,1,21102,588,1,0,1106,0,1378,1102,1,758,594,101,0,0,753,1006,753,654,21002,753,1,1,21102,1,610,0,1105,1,667,21101,0,0,1,21102,1,621,0,1105,1,1463,1205,1,647,21101,0,1015,1,21102,635,1,0,1106,0,1378,21102,1,1,1,21102,646,1,0,1106,0,1463,99,1001,594,1,594,1105,1,592,1006,755,664,1101,0,0,755,1105,1,647,4,754,99,109,2,1101,0,726,757,21202,-1,1,1,21101,0,9,2,21102,1,697,3,21102,692,1,0,1106,0,1913,109,-2,2106,0,0,109,2,1002,757,1,706,2101,0,-1,0,1001,757,1,757,109,-2,2105,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,255,63,95,191,223,127,159,0,175,253,140,172,157,76,186,169,188,162,184,51,219,236,70,137,68,178,114,187,61,215,156,54,93,49,100,125,252,251,34,87,110,242,220,254,189,111,182,177,232,35,59,154,62,190,170,222,173,69,57,227,43,233,206,216,85,247,101,179,58,115,226,113,244,241,234,237,155,207,158,168,92,84,153,196,86,47,200,183,77,79,121,243,118,250,221,230,46,50,202,201,102,38,212,141,239,116,245,166,217,108,199,39,174,248,71,231,124,117,103,120,238,126,55,99,214,228,106,142,53,119,42,185,138,204,218,197,198,249,122,229,171,139,94,56,246,203,123,163,205,152,107,143,167,98,60,235,109,78,213,181,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,73,110,112,117,116,32,105,110,115,116,114,117,99,116,105,111,110,115,58,10,13,10,87,97,108,107,105,110,103,46,46,46,10,10,13,10,82,117,110,110,105,110,103,46,46,46,10,10,25,10,68,105,100,110,39,116,32,109,97,107,101,32,105,116,32,97,99,114,111,115,115,58,10,10,58,73,110,118,97,108,105,100,32,111,112,101,114,97,116,105,111,110,59,32,101,120,112,101,99,116,101,100,32,115,111,109,101,116,104,105,110,103,32,108,105,107,101,32,65,78,68,44,32,79,82,44,32,111,114,32,78,79,84,67,73,110,118,97,108,105,100,32,102,105,114,115,116,32,97,114,103,117,109,101,110,116,59,32,101,120,112,101,99,116,101,100,32,115,111,109,101,116,104,105,110,103,32,108,105,107,101,32,65,44,32,66,44,32,67,44,32,68,44,32,74,44,32,111,114,32,84,40,73,110,118,97,108,105,100,32,115,101,99,111,110,100,32,97,114,103,117,109,101,110,116,59,32,101,120,112,101,99,116,101,100,32,74,32,111,114,32,84,52,79,117,116,32,111,102,32,109,101,109,111,114,121,59,32,97,116,32,109,111,115,116,32,49,53,32,105,110,115,116,114,117,99,116,105,111,110,115,32,99,97,110,32,98,101,32,115,116,111,114,101,100,0,109,1,1005,1262,1270,3,1262,20101,0,1262,0,109,-1,2106,0,0,109,1,21101,0,1288,0,1105,1,1263,21002,1262,1,0,1102,0,1,1262,109,-1,2105,1,0,109,5,21102,1,1310,0,1105,1,1279,22101,0,1,-2,22208,-2,-4,-1,1205,-1,1332,22102,1,-3,1,21101,0,1332,0,1106,0,1421,109,-5,2106,0,0,109,2,21101,0,1346,0,1105,1,1263,21208,1,32,-1,1205,-1,1363,21208,1,9,-1,1205,-1,1363,1106,0,1373,21101,1370,0,0,1105,1,1279,1105,1,1339,109,-2,2105,1,0,109,5,2101,0,-4,1385,21001,0,0,-2,22101,1,-4,-4,21102,1,0,-3,22208,-3,-2,-1,1205,-1,1416,2201,-4,-3,1408,4,0,21201,-3,1,-3,1105,1,1396,109,-5,2105,1,0,109,2,104,10,22102,1,-1,1,21102,1436,1,0,1106,0,1378,104,10,99,109,-2,2105,1,0,109,3,20002,594,753,-1,22202,-1,-2,-1,201,-1,754,754,109,-3,2105,1,0,109,10,21101,5,0,-5,21101,1,0,-4,21102,0,1,-3,1206,-9,1555,21101,3,0,-6,21102,5,1,-7,22208,-7,-5,-8,1206,-8,1507,22208,-6,-4,-8,1206,-8,1507,104,64,1105,1,1529,1205,-6,1527,1201,-7,716,1515,21002,0,-11,-8,21201,-8,46,-8,204,-8,1105,1,1529,104,46,21201,-7,1,-7,21207,-7,22,-8,1205,-8,1488,104,10,21201,-6,-1,-6,21207,-6,0,-8,1206,-8,1484,104,10,21207,-4,1,-8,1206,-8,1569,21101,0,0,-9,1105,1,1689,21208,-5,21,-8,1206,-8,1583,21101,0,1,-9,1106,0,1689,1201,-5,716,1588,21001,0,0,-2,21208,-4,1,-1,22202,-2,-1,-1,1205,-2,1613,22101,0,-5,1,21101,1613,0,0,1106,0,1444,1206,-1,1634,21202,-5,1,1,21102,1627,1,0,1106,0,1694,1206,1,1634,21102,2,1,-3,22107,1,-4,-8,22201,-1,-8,-8,1206,-8,1649,21201,-5,1,-5,1206,-3,1663,21201,-3,-1,-3,21201,-4,1,-4,1106,0,1667,21201,-4,-1,-4,21208,-4,0,-1,1201,-5,716,1676,22002,0,-1,-1,1206,-1,1686,21101,0,1,-4,1105,1,1477,109,-10,2106,0,0,109,11,21101,0,0,-6,21101,0,0,-8,21101,0,0,-7,20208,-6,920,-9,1205,-9,1880,21202,-6,3,-9,1201,-9,921,1725,20102,1,0,-5,1001,1725,1,1733,20102,1,0,-4,21202,-4,1,1,21101,1,0,2,21101,0,9,3,21102,1,1754,0,1106,0,1889,1206,1,1772,2201,-10,-4,1766,1001,1766,716,1766,21002,0,1,-3,1106,0,1790,21208,-4,-1,-9,1206,-9,1786,21201,-8,0,-3,1106,0,1790,21201,-7,0,-3,1001,1733,1,1796,20102,1,0,-2,21208,-2,-1,-9,1206,-9,1812,21201,-8,0,-1,1105,1,1816,22101,0,-7,-1,21208,-5,1,-9,1205,-9,1837,21208,-5,2,-9,1205,-9,1844,21208,-3,0,-1,1105,1,1855,22202,-3,-1,-1,1105,1,1855,22201,-3,-1,-1,22107,0,-1,-1,1106,0,1855,21208,-2,-1,-9,1206,-9,1869,21202,-1,1,-8,1105,1,1873,21202,-1,1,-7,21201,-6,1,-6,1105,1,1708,22102,1,-8,-10,109,-11,2106,0,0,109,7,22207,-6,-5,-3,22207,-4,-6,-2,22201,-3,-2,-1,21208,-1,0,-6,109,-7,2105,1,0,0,109,5,1201,-2,0,1912,21207,-4,0,-1,1206,-1,1930,21101,0,0,-4,22102,1,-4,1,21202,-3,1,2,21101,0,1,3,21102,1,1949,0,1106,0,1954,109,-5,2105,1,0,109,6,21207,-4,1,-1,1206,-1,1977,22207,-5,-3,-1,1206,-1,1977,22102,1,-5,-5,1105,1,2045,22101,0,-5,1,21201,-4,-1,2,21202,-3,2,3,21101,0,1996,0,1106,0,1954,22101,0,1,-5,21101,1,0,-2,22207,-5,-3,-1,1206,-1,2015,21101,0,0,-2,22202,-3,-2,-3,22107,0,-4,-1,1206,-1,2037,22102,1,-2,1,21102,2037,1,0,106,0,1912,21202,-3,-1,-3,22201,-5,-3,-5,109,-6,2106,0,0] # noqa
# fmt: on


# In[2]:


# OPCODE INT MACHINE


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


# if one_output=False --> returns OUTPUT - array of outputs
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
            i = i + 2
            if input_index < len(input_signals) - 1:
                input_index += 1
            else:
                input_index += 0
                # print("no more input signals")
                if one_output:
                    return (
                        output,
                        dictcode,
                        i,
                        input_signals,
                        input_index,
                        relative_base,
                    )
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


# In[3]:


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


def run_program(all_inputs):
    dictcode = code_to_dictcode(puzzle_input)
    i = 0
    relative_base = 0
    command = all_inputs.pop(0)
    print("**", command, "**")
    input_signals = to_ascii(command)
    # print("***",input_signals)
    input_index = 0

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

        # print(from_ascii(answer))
        if output == "HALT":
            # print(answer)
            print(from_ascii(answer))
            print("GAME OVER")
            break

        if len(all_inputs) > 0:
            command = all_inputs.pop(0)
            print(command)
            input_signals = to_ascii(command)
        else:
            aa = ""  # input()
            input_signals = to_ascii(aa)
        input_index = 0
        # print("***",input_signals)
    return 0


# In[4]:


# PART 1

# check that D is not a hole
# jump if C is a hole
# jump if A is a hole

all_inputs = """NOT C J
AND D J
NOT A T
OR T J
WALK
""".splitlines()

# run_program(all_inputs)


# In[12]:


# PART 2 - registers go to I

# always check H D
# 1. check H D
# jump if C is a hole
# 2. check H D
# jump if B is a hole
# 3. jump if A is a hole, always

# NOT C J
# AND D J
# AND H J

# NOT B T
# AND D T
# AND H T
# OR T J

# NOT A T
# OR T J

all_inputs = """NOT C J
AND D J
AND H J
NOT B T
AND D T
AND H T
OR T J
NOT A T
OR T J
RUN
""".splitlines()

run_program(all_inputs)

raise

# In[60]:


# failed attempt at brute force

part_one = ["AND", "OR", "NOT"]
part_two = ["A", "B", "C", "D", "T", "J"]
part_three = ["T", "J"]

# instruction = (i,j,k)


def build_random_script():
    ret = []
    length = np.random.randint(5, 15)
    for i in range(length):
        ret.append(build_random_instruction())
    return ret


def script_to_commands(ss):
    cd = []
    for s in ss:
        cd.append(instruction_to_input(s))
    cd.append("RUN")
    return cd


def build_random_instruction():
    return (
        np.random.randint(len(part_one)),
        np.random.randint(len(part_two)),
        np.random.randint(len(part_three)),
    )


def instruction_to_input(instruction):
    return (
        part_one[instruction[0]]
        + " "
        + part_two[instruction[1]]
        + " "
        + part_three[instruction[2]]
    )


def mutate_instruction(instruction):
    dice = np.random.randint(3)
    if dice == 0:
        return np.random.randint(len(part_one)), instruction[1], instruction[2]
    elif dice == 1:
        return instruction[0], np.random.randint(len(part_two)), instruction[2]
    elif dice == 2:
        return instruction[0], instruction[1], np.random.randint(len(part_three))


def crossover(inst1, inst2):
    dice = np.random.randint(2)
    if dice == 0:
        return inst1[0], inst2[1], inst2[2]
    elif dice == 1:
        return inst1[0], inst1[1], inst2[2]


SIZE = 100
np.random.seed(42)
population = []  # type: ignore
for j in range(SIZE):
    population.append(build_random_script())

for s in population:
    cds = script_to_commands(s)
    run_program(cds)

# NEED TO SCORE...
