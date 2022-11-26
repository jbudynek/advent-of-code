from timeit import default_timer as timer
import pickle

# Constants
##########

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'

RED_BG = '\x1b[101m'
GREEN_BG = '\x1b[102m'
YELLOW_BG = '\x1b[103m'
DEFAULT_BG = '\x1b[49m'

# Helpers
#########

def read_input_file(input_file):
    f = open(input_file, "r")
    contents = f.read()
    puzzle_input = contents.splitlines()
    f.close()
    return puzzle_input


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end-t_start
    print(int(s*1000), "ms = ", int(s), "s = ", int(s/60), "min")


RED_FG = '\x1b[91m'
GREEN_FG = '\x1b[92m'
YELLOW_FG = '\x1b[93m'
DEFAULT_FG = '\x1b[39m'


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = (result == expected)
    sflag = ""
    if flag == True:
        sflag = GREEN_FG+str(flag)+DEFAULT_FG
    else:
        sflag = RED_FG+str(flag)+DEFAULT_FG

    if(expected == "None"):
        print("*** "+str(cc) + " *** -> Result = "+str(result))
    else:
        print("*** "+str(cc) + " *** -> Result = "+str(result) +
              " -> success = " + sflag + " -> expected " + expected)
    print_time(t_start, t_end)
    return flag


def test_func(func, cc=None, expected=None, DBG=False):
    t_start = timer()
    result = func(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)

def run_func(func, puzzle_input, DBG=False):
    t_start = timer()
    ret = func(puzzle_input, DBG=False)
    t_end = timer()
    print_time(t_start, t_end)
    print(ret)
