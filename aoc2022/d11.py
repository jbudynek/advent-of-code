# coding: utf-8
import re
import sys
from collections import deque
from math import prod

from boilerplate import read_input_file, run_func, test_func


def get_first_int(line):
    return list(map(int, re.findall(r"-?\d+", line)))[0]


class Monkey:
    def __init__(self, id, items, operation, divisor, test_true, test_false):
        self.id = id
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.test_true = test_true
        self.test_false = test_false
        self.count_inspections = 0

        # parse operation and wire to appropriate function
        # v holds the value to add or multiply with
        # we could use "eval", it would be simpler but a bit slower
        if "+" in self.operation:
            v = get_first_int(self.operation)
            self.f = self.add
            self.v = v
        elif "old * old" in self.operation:
            self.f = self.sq
            self.v = 0
        elif "*" in self.operation:
            v = get_first_int(self.operation)
            self.f = self.mul
            self.v = v
        else:
            print("parsing error")
            sys.exit()

    def add(self, x):
        return x + self.v

    def mul(self, x):
        return x * self.v

    def sq(self, x):
        return x * x

    def compute_operation(self, item):
        return self.f(item)

    def test(self, item):
        return item % self.divisor == 0


def parse_monkeys(input_val):

    monkeys = {}

    all_divisors = []

    id = 0
    items = deque()
    operation = ""
    divisor = 0
    test_true = 0
    test_false = 0
    for line in input_val:
        if "Monkey" in line:
            id = get_first_int(line)
        elif "Starting" in line:  # dequeue is overkill as there are only a few items
            items = deque(map(int, re.findall(r"-?\d+", line)))
        elif "Operation" in line:
            operation = line.split("=")[1]
        elif "Test" in line:
            divisor = get_first_int(line)
            all_divisors.append(divisor)
        elif "If true" in line:
            test_true = get_first_int(line)
        elif "If false" in line:
            test_false = get_first_int(line)
        elif line == "":
            m = Monkey(id, items, operation, divisor, test_true, test_false)
            monkeys[id] = m
            id = 0
            items = deque()
            operation = ""
            divisor = 0
            test_true = 0
            test_false = 0
        else:
            print("parsing error")
            sys.exit()

    m = Monkey(id, items, operation, divisor, test_true, test_false)
    monkeys[id] = m

    # we should use least common multiple instead of product,
    # but it works! because all divisors are prime.
    return monkeys, prod(all_divisors)


def run_rounds(monkeys, nb_rounds, div, modulo):
    nbm = len(monkeys.values())
    for _ in range(nb_rounds):
        for i in range(nbm):
            m = monkeys[i]
            while len(m.items) > 0:
                item = m.items.popleft()
                item = m.compute_operation(item)
                m.count_inspections += 1
                if div:  # for part 1
                    item = item // 3
                else:  # for part 2
                    item = item % modulo
                if m.test(item):
                    monkeys[m.test_true].items.append(item)
                else:
                    monkeys[m.test_false].items.append(item)
    nb_inspections = []
    for m in monkeys.values():
        nb_inspections.append(m.count_inspections)

    return prod(sorted(nb_inspections)[-2:])


def boom_part1(input_val, DBG=True):
    monkeys, _ = parse_monkeys(input_val)
    return run_rounds(monkeys, 20, True, 0)


def boom_part2(input_val, DBG=True):
    monkeys, modulo = parse_monkeys(input_val)
    return run_rounds(monkeys, 10000, False, modulo)


# Test cases
##########


t1 = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 10605, True)
test_func(boom_part2, tt1, 2713310158, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d11.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 78678
# PART 2 OK = 15333249714
