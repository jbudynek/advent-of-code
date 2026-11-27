# Algorithm (code written by MAI Code 2 Flash, a GitHub Copilot coding model):
# - Part 1: interpret the Duet instructions, keeping the most recently played
#   sound and stopping on the first non-zero rcv.
# - Part 2: run two copies independently with separate registers and queues.
#   Execute one instruction at a time in round-robin order, blocking a program
#   only when rcv finds an empty queue; stop at mutual deadlock or termination.

from collections import deque

ipt_test = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

ipt_test2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

ipt_puzzle = open("input.txt").read().strip()


def value(token, registers):
    if token.isalpha():
        return registers.get(token, 0)
    return int(token)


def duet(text):
    instructions = [line.split() for line in text.splitlines()]
    registers = {}
    last_sound = None
    pc = 0

    while 0 <= pc < len(instructions):
        parts = instructions[pc]
        opcode = parts[0]
        x = parts[1]

        if opcode == "snd":
            last_sound = value(x, registers)
        elif opcode == "set":
            registers[x] = value(parts[2], registers)
        elif opcode == "add":
            registers[x] = value(x, registers) + value(parts[2], registers)
        elif opcode == "mul":
            registers[x] = value(x, registers) * value(parts[2], registers)
        elif opcode == "mod":
            registers[x] = value(x, registers) % value(parts[2], registers)
        elif opcode == "rcv":
            if value(x, registers) != 0:
                return last_sound
        elif opcode == "jgz":
            if value(x, registers) > 0:
                pc += value(parts[2], registers)
                continue

        pc += 1

    return last_sound


def duet2(text):
    instructions = [line.split() for line in text.splitlines()]
    registers = [{"p": 0}, {"p": 1}]
    queues = [deque(), deque()]
    pcs = [0, 0]
    sent_by_one = 0

    while True:
        progressed = False

        for program in (0, 1):
            pc = pcs[program]
            if not 0 <= pc < len(instructions):
                continue

            parts = instructions[pc]
            opcode = parts[0]
            x = parts[1]
            target = registers[program]

            if opcode == "snd":
                queues[1 - program].append(value(x, target))
                if program == 1:
                    sent_by_one += 1
                pcs[program] += 1
                progressed = True
            elif opcode == "set":
                target[x] = value(parts[2], target)
                pcs[program] += 1
                progressed = True
            elif opcode == "add":
                target[x] = value(x, target) + value(parts[2], target)
                pcs[program] += 1
                progressed = True
            elif opcode == "mul":
                target[x] = value(x, target) * value(parts[2], target)
                pcs[program] += 1
                progressed = True
            elif opcode == "mod":
                target[x] = value(x, target) % value(parts[2], target)
                pcs[program] += 1
                progressed = True
            elif opcode == "rcv":
                if queues[program]:
                    target[x] = queues[program].popleft()
                    pcs[program] += 1
                    progressed = True
            elif opcode == "jgz":
                if value(x, target) > 0:
                    pcs[program] += value(parts[2], target)
                else:
                    pcs[program] += 1
                progressed = True

        if not progressed:
            return sent_by_one

        terminated = all(not (0 <= pcs[i] < len(instructions)) for i in (0, 1))
        if terminated:
            return sent_by_one

        blocked = [
            0 <= pcs[i] < len(instructions)
            and instructions[pcs[i]][0] == "rcv"
            and not queues[i]
            for i in (0, 1)
        ]
        if all(blocked[i] or not (0 <= pcs[i] < len(instructions)) for i in (0, 1)):
            return sent_by_one


# test part 1
r_test1 = duet(ipt_test)
print(f"# Test part 1: {r_test1} (expected 4)")
assert r_test1 == 4

r1 = duet(ipt_puzzle)
print(f"# Part 1 solution: {r1}")

# test part 2
r_test2 = duet2(ipt_test2)
print(f"# Test part 2: {r_test2} (expected 3)")
assert r_test2 == 3

r2 = duet2(ipt_puzzle)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 9423
# Part 2 solution: 7620
