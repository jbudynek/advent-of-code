INPUT_FILE = "input-d03.txt"
with open(INPUT_FILE) as f:
    inputs = f.readlines()

# inputs=['>'] #2
# inputs=['^>v<'] #4
# inputs=['^v^v^v^v^v'] #2


def increase(h2p, xx, yy):
    if (xx, yy) not in h2p:
        h2p[(xx, yy)] = 0
    h2p[(xx, yy)] = h2p[(xx, yy)] + 1


def process(house_to_pres, s):

    cur_x = 0
    cur_y = 0

    increase(house_to_pres, cur_x, cur_y)

    for c in s:
        if c == ">":
            cur_x = cur_x + 1
        elif c == "<":
            cur_x = cur_x - 1
        elif c == "^":
            cur_y = cur_y + 1
        else:
            cur_y = cur_y - 1
        increase(house_to_pres, cur_x, cur_y)

    return house_to_pres


house_to_pres: dict[tuple, int] = {}

nb_pres = len(process(house_to_pres, inputs[0]))

print(nb_pres)

##

house_to_pres = {}

santa = inputs[0][0::2]
robot = inputs[0][1::2]

house_to_pres = process(house_to_pres, santa)
house_to_pres = process(house_to_pres, robot)

nb_pres = len(house_to_pres)
print(nb_pres)
