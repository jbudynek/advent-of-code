ipt = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".splitlines()

ipt = open("input.txt").read().splitlines()

result1, result2 = 0, 0
all_numbers, all_targets = [], []

for line in ipt:
    s = line.split(":")
    target = int(s[0])
    numbers = [int(e) for e in s[1].split()]
    all_numbers.append(numbers)
    all_targets.append(target)


def is_possible(target, numbers, part):
    if len(numbers) == 1:
        return target == numbers[0]
    n = numbers[-1]
    n2 = numbers.copy()
    del n2[-1]
    if target % n == 0:
        if is_possible(target // n, n2, part):
            return True
    if target - n >= 0:
        if is_possible(target - n, n2, part):
            return True
    if part == 2:
        if len(numbers) == 2:
            n = int(str(numbers[-2]) + str(numbers[-1]))
            if n == target:
                return True
        if len(numbers) > 2:
            last = str(numbers[-1])
            if str(target).endswith(last):
                n2 = numbers.copy()
                del n2[-1]
                t2 = int(str(target).removesuffix(last))
                if is_possible(t2, n2, part):
                    return True
    return False


for i, target in enumerate(all_targets):
    if is_possible(target, all_numbers[i], 1):
        result1 += target
    if is_possible(target, all_numbers[i], 2):
        result2 += target

print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

# Part 1 solution: 3245122495150
# Part 2 solution: 105517128211543
