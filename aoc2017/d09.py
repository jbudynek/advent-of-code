#ipt_test = """{{<a!>},{<a!>},{<a!>},{<ab>}}"""

ipt_puzzle = open("input.txt").read()

#ipt=ipt_test
ipt = ipt_puzzle

no_bang = ""
idx=0
while idx <(len(ipt)):
    c=ipt[idx]
    if c=="!":
        idx+=1
    else:
        no_bang +=c
    idx +=1

score = 0
depth = 0
idx = 0
count_garbage=0
while idx <(len(no_bang)):
    c=no_bang[idx]
    if c == '{':
        depth += 1
    elif c=="}":
        score += depth
        depth -=1
    elif c=="<":
        while no_bang[idx]!=">":
            count_garbage+=1
            idx +=1
        count_garbage-=1
    idx +=1
    
print(f"# Part 1 solution: {score}")
print(f"# Part 2 solution: {count_garbage}")

# Part 1 solution: 14421
# Part 2 solution: 6817