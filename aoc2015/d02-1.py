INPUT_FILE = "input-d02.txt"
with open(INPUT_FILE) as f:
    inputs = f.readlines()

# inputs=['2x3x4'] #58
# inputs=['1x1x10'] #42


def process(s):
    ss = s.split("x")
    width = int(ss[0])
    length = int(ss[1])
    height = int(ss[2])
    # 2*l*w + 2*w*h + 2*h*l
    s1 = length * width
    s2 = width * height
    s3 = height * length

    surf = 2 * s1 + 2 * s2 + 2 * s3 + min(s1, min(s2, s3))
    return surf


surface = 0
for pp in inputs:
    surface = surface + process(pp)

print(surface)

##

# inputs=['2x3x4'] #34
# inputs=['1x1x10'] #14


def process_ribbon(s):
    ss = s.split("x")
    si = [int(numeric_string) for numeric_string in ss]
    si.sort()
    ll = 2 * si[0] + 2 * si[1] + (si[0] * si[1] * si[2])
    return ll


length = 0
for pp in inputs:
    length = length + process_ribbon(pp)

print(length)
