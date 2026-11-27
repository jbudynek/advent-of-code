# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: execute the coprocessor instructions, reading registers or integer
#   literals, and count every mul operation until the program leaves the code.

ipt_test = """set x 2
mul x 3
jnz x 2
set x 99
set x 0"""

ipt_puzzle = open("input.txt").read().strip()


def value(registers, operand):
    return int(operand) if operand.lstrip("-").isdigit() else registers[operand]


def mul_count(text):
    instructions = [line.split() for line in text.splitlines()]
    registers = {chr(code): 0 for code in range(ord("a"), ord("h") + 1)}
    registers["a"] = 0
    position = 0
    count = 0

    while 0 <= position < len(instructions):
        operation, x, y = instructions[position]
        if operation == "set":
            registers[x] = value(registers, y)
        elif operation == "sub":
            registers[x] -= value(registers, y)
        elif operation == "mul":
            registers[x] *= value(registers, y)
            count += 1
        elif operation == "jnz":
            if value(registers, x) != 0:
                position += value(registers, y)
                continue
        position += 1

    return count


# test
r_test1 = mul_count(ipt_test)
print(f"# Test part 1: {r_test1} (expected 1)")
assert r_test1 == 1

r1 = mul_count(ipt_puzzle)
print(f"# Part 1 solution: {r1}")


# - Part 2: the debug-mode program counts composite values in the arithmetic
#   progression starting at 109900, ending at 126900, in steps of 17; test each
#   value directly instead of executing the nested-loop program for billions of steps.

def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def optimized_h(text):
    instructions = [line.split() for line in text.splitlines()]
    registers = {chr(code): 0 for code in range(ord("a"), ord("h") + 1)}
    registers["a"] = 1
    position = 0

    while position < 8:
        operation, x, y = instructions[position]
        if operation == "set":
            registers[x] = value(registers, y)
        elif operation == "sub":
            registers[x] -= value(registers, y)
        elif operation == "mul":
            registers[x] *= value(registers, y)
        elif operation == "jnz" and value(registers, x) != 0:
            position += value(registers, y)
            continue
        position += 1

    start = registers["b"]
    end = registers["c"]
    return sum(not is_prime(number) for number in range(start, end + 1, 17))


r_test2 = is_prime(2)
assert r_test2 is True
assert is_prime(9) is False

r2 = optimized_h(ipt_puzzle)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 9409
# Part 2 solution: 913
