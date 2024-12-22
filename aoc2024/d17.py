import re

ipt = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".split(
    "\n\n"
)


ipt = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""".split(
    "\n\n"
)

ipt = open("input-d17.txt").read().split("\n\n")

registers = {}
for line in ipt[0].split("\n"):
    ll = line.split(":")
    r = ll[0][-1]
    v = int(ll[1])
    registers[r] = v

program = list(map(int, re.findall(r"-?\d+", ipt[1])))


def run(program, registers):
    # print("run")
    # print(",".join([str(e) for e in program]))
    # print(registers)
    output = []
    inst_prt = 0
    while inst_prt < len(program):
        instruction, literal_operand = program[inst_prt], program[inst_prt + 1]
        combo_operand = literal_operand
        if literal_operand == 4:
            combo_operand = registers["A"]
        elif literal_operand == 5:
            combo_operand = registers["B"]
        elif literal_operand == 6:
            combo_operand = registers["C"]

        if instruction == 0:  # adv = A division 2^combo
            ret = registers["A"] // 2**combo_operand
            registers["A"] = ret
        elif instruction == 1:  # bxl = B Xor literal
            ret = registers["B"] ^ literal_operand
            registers["B"] = ret
        elif instruction == 2:  # bst = combo mod 8
            ret = combo_operand % 8
            registers["B"] = ret
        elif instruction == 3:  # jnz = jump if a not zero
            if not registers["A"] == 0:
                inst_prt = literal_operand - 2
        elif instruction == 4:  # bxc = b^c
            ret = registers["B"] ^ registers["C"]
            registers["B"] = ret
        elif instruction == 5:  # out = combo % 8
            output.append((combo_operand % 8))
        elif instruction == 6:  # bdv = division
            ret = registers["A"] // 2**combo_operand
            registers["B"] = ret
        elif instruction == 7:  # cdv = division
            ret = registers["A"] // 2**combo_operand
            registers["C"] = ret

        inst_prt += 2

    return output


r1 = run(program, registers)


def find(a, i):
    registers["A"] = a
    registers["B"] = 0
    registers["C"] = 0
    out = run(program, registers)
    if out == program:
        return a
    # if we start, or if we know how to produce i last numbers
    elif (i == 0) or (out == program[-i:]):
        for n in range(8):
            # shift
            r = find(8 * a + n, i + 1)
            if r is not None:
                return r
    return None


r2 = find(0, 0)

print(f"# Part 1 solution: {','.join([str(e) for e in r1])}")
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 7,1,3,7,5,1,0,3,4
# Part 2 solution: 190384113204239
