from timeit import default_timer as timer  # noqa: F401


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


# Example (from a dNN.py in a year folder, run as `python dNN.py`):
#
#   import sys
#
#   sys.path.append("../tools")
#   from timing import print_time, timer
#
#   t_start = timer()
#   print(solve_part2(puzzle_input))
#   t_end = timer()
#   print_time(t_start, t_end)  # e.g. "6120 ms =  6 s =  0 min"
