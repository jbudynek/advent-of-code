# coding: utf-8
from boilerplate import read_input_file, run_func, test_func


def find_starter(message, starter_length):
    for i in range(len(message) - starter_length):
        if len(set(message[i : i + starter_length])) == starter_length:  # noqa
            return i + starter_length
    return -1


def boom_part1(input_val, DBG=True):
    return find_starter(input_val[0], 4)


def boom_part2(input_val, DBG=True):
    return find_starter(input_val[0], 14)


# Test cases
##########


t1 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 5, True)
t1 = "nppdvjthqldpwncqszvftbrmjlhg"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 6, True)
t1 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 10, True)
t1 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 11, True)

t1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 19, True)
t1 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 23, True)
t1 = "nppdvjthqldpwncqszvftbrmjlhg"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 23, True)
t1 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 29, True)
t1 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
tt1 = t1.splitlines()
test_func(boom_part2, tt1, 26, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d06.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 1833
# PART 2 OK = 3425
