ipt_test = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""".splitlines()

ipt_puzzle = open("input.txt").read().splitlines()

#ipt=ipt_test
ipt = ipt_puzzle

def parse(line):
  delta = int(line[1:])
  nb_rot = delta//100 
  delta = delta%100
  direction = 1
  if line[0] == "L":
    direction = -1

  return delta,nb_rot,direction

pointer = 50
prev_pointer=0
p1=0
p2=0
for line in ipt:
  prev_pointer=pointer
  delta,tour,sens = parse(line)
  pointer+=(delta*sens)
  p2+=tour
  if prev_pointer<100 and pointer>=100:
    p2+=1
  elif prev_pointer>0 and pointer<=0:
    p2+=1

  if pointer<0:
    pointer+=100
  if pointer>=100:
    pointer-=100

  if pointer==0:p1+=1

print(f"# Part 1 solution: {(p1)}")
print(f"# Part 2 solution: {(p2)}")

# Part 1 solution: 997
# Part 2 solution: 5978
