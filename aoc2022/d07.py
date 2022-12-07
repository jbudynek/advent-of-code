# coding: utf-8

from boilerplate import read_input_file, run_func, test_func


class F:
    """This class represents a file, we only need to store its size."""

    def __init__(self, size):
        self.size = size


class D(F):
    """This class represents a directory, it contains a list of files."""

    def __init__(self, parent, size):
        self.parent = parent
        self.files = []
        super().__init__(size)


def compute_dir_size(root):
    if isinstance(root, D):
        for f in root.files:
            root.size += compute_dir_size(f)
    return root.size


def parse_dirs(input_val):
    root = D(None, 0)
    cur_node = root
    del input_val[0]
    for line in input_val:
        if line.startswith("dir"):
            pass
        elif line.startswith("$ cd .."):
            cur_node = cur_node.parent
        elif line.startswith("$ cd"):
            d = D(cur_node, 0)
            cur_node.files.append(d)
            cur_node = d
        elif line.startswith("$ ls"):
            pass
        else:  # size(int) name(str)
            ll = line.split()
            f = F(int(ll[0]))
            cur_node.files.append(f)

    compute_dir_size(root)
    return root


def find_biggest_dirs(tree, max_size):
    ret = []
    if isinstance(tree, D):
        if tree.size <= max_size:
            ret.append(tree)
        for f in tree.files:
            ret.extend(find_biggest_dirs(f, max_size))
    return ret


def boom_part1(input_val, DBG=True):
    tree = parse_dirs(input_val)
    biggest_dirs = find_biggest_dirs(tree, 100000)
    all_dir_size = [dir.size for dir in biggest_dirs]
    return sum(all_dir_size)


def boom_part2(input_val, DBG=True):
    tree = parse_dirs(input_val)
    total_size = 70000000
    free_space = total_size - tree.size
    biggest_dirs = find_biggest_dirs(tree, total_size)
    ret = [d.size for d in biggest_dirs if free_space + d.size > 30000000]
    return min(ret)


# Test cases
##########


t1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
tt1 = t1.splitlines()
test_func(boom_part1, tt1, 95437, True)
test_func(boom_part2, tt1, 24933642, True)
# sys.exit()

# Real data
##########

puzzle_input = read_input_file("input-d07.txt")

# part 1

run_func(boom_part1, puzzle_input, DBG=False)

# part 2

run_func(boom_part2, puzzle_input, DBG=False)

# PART 1 OK = 1501149
# PART 2 OK = 10096985
