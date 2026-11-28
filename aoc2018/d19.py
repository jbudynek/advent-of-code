# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model)
# Execute the bound-instruction-pointer program by applying each named opcode to six registers.
# Part 2 reaches a large target in register 4; its answer is the sum of that target's divisors,
# avoiding billions of iterations through the nested factor-testing loop.

ipt_test = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

ipt_puzzle = open("input.txt").read().strip()


def execute_opcode(name, a, b, c, registers):
    result = registers.copy()
    if name == "addr":
        result[c] = registers[a] + registers[b]
    elif name == "addi":
        result[c] = registers[a] + b
    elif name == "mulr":
        result[c] = registers[a] * registers[b]
    elif name == "muli":
        result[c] = registers[a] * b
    elif name == "banr":
        result[c] = registers[a] & registers[b]
    elif name == "bani":
        result[c] = registers[a] & b
    elif name == "borr":
        result[c] = registers[a] | registers[b]
    elif name == "bori":
        result[c] = registers[a] | b
    elif name == "setr":
        result[c] = registers[a]
    elif name == "seti":
        result[c] = a
    elif name == "gtir":
        result[c] = int(a > registers[b])
    elif name == "gtri":
        result[c] = int(registers[a] > b)
    elif name == "gtrr":
        result[c] = int(registers[a] > registers[b])
    elif name == "eqir":
        result[c] = int(a == registers[b])
    elif name == "eqri":
        result[c] = int(registers[a] == b)
    elif name == "eqrr":
        result[c] = int(registers[a] == registers[b])
    else:
        raise ValueError(name)
    return result


def run_program(program, initial_registers=None, max_steps=None):
    lines = program.strip().splitlines()
    ip_register = int(lines[0].split()[1])
    instructions = [line.split() for line in lines[1:]]
    registers = initial_registers.copy() if initial_registers is not None else [0] * 6
    ip = 0
    steps = 0

    while 0 <= ip < len(instructions):
        if max_steps is not None and steps >= max_steps:
            break
        registers[ip_register] = ip
        name, a, b, c = instructions[ip]
        registers = execute_opcode(name, int(a), int(b), int(c), registers)
        ip = registers[ip_register] + 1
        steps += 1

    return registers


def divisor_sum(number):
    total = 0
    for divisor in range(1, int(number ** 0.5) + 1):
        if number % divisor == 0:
            total += divisor
            paired = number // divisor
            if paired != divisor:
                total += paired
    return total


assert run_program(ipt_test)[0] == 6
assert divisor_sum(36) == 91

part1 = run_program(ipt_puzzle)[0]
part2_state = run_program(ipt_puzzle, [1, 0, 0, 0, 0, 0], 100_000)
part2 = divisor_sum(part2_state[4])

print("Part 1:", part1)
print("Part 2:", part2)

# Part 1 solution: 1392
# Part 2 solution: 15826992
