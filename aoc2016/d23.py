# Algorithm (code written by Claude, an AI assistant made by Anthropic)
# Part 1: an assembunny interpreter (cpy/inc/dec/jnz) extended with tgl, which
# rewrites the instruction list in place (inc<->dec, tgl->inc, jnz<->cpy). Invalid
# instructions (e.g. cpy with a non-register target) are skipped. Start with a=7.
# Part 2: same program with a=12 is too slow naively, so the interpreter has a
# peephole optimisation: the pattern "inc x / dec y / jnz y -2" (in either order)
# (and its toggled variants with dec x) is the loop x += y; y = 0, executed in one step. The nested loops thus
# become multiplications and the program finishes instantly. A second peephole folds
# the whole 6-line multiplication loop "cpy x c / inc a / dec c / jnz c -2 / dec d /
# jnz d -5" into a += x * d.

ipt_test = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
ipt_puzzle = open("input.txt").read().strip()

TOGGLE = {"inc": "dec", "dec": "inc", "tgl": "inc", "jnz": "cpy", "cpy": "jnz"}


def run(ipt, a):
    prog = [l.split() for l in ipt.splitlines()]
    reg = {"a": a, "b": 0, "c": 0, "d": 0}

    def val(x):
        return reg[x] if x in reg else int(x)

    pc = 0
    while 0 <= pc < len(prog):
        ins = prog[pc]
        op = ins[0]
        # peephole: multiplication "cpy x c / inc a / dec c / jnz c -2 / dec d / jnz d -5"
        if (op == "cpy" and pc + 5 < len(prog) and ins[2] in reg):
            i1, i2, i3, i4, i5 = prog[pc + 1:pc + 6]
            c, a_, d_ = ins[2], i1[-1], i4[-1]
            if (i1[0] in ("inc", "dec") and i2 == ["dec", c] and i3 == ["jnz", c, "-2"]
                    and i4[0] == "dec" and i5 == ["jnz", d_, "-5"]
                    and len({c, a_, d_}) == 3 and a_ in reg and d_ in reg
                    and len(i1) == 2 and len(i4) == 2):
                sign = 1 if i1[0] == "inc" else -1
                reg[a_] += sign * val(ins[1]) * reg[d_]
                reg[c] = 0
                reg[d_] = 0
                pc += 6
                continue
        # peephole: addition/subtraction loop
        if pc + 2 < len(prog):
            p, q, r = prog[pc:pc + 3]
            if (r[0] == "jnz" and r[2] == "-2" and r[1] in reg
                    and p[0] in ("inc", "dec") and q[0] in ("inc", "dec")
                    and len(p) == 2 and len(q) == 2):
                # the loop counter is the register that is decremented and tested
                for other, ctr in ((p, q), (q, p)):
                    if ctr[0] == "dec" and ctr[1] == r[1] and other[1] in reg and other[1] != ctr[1]:
                        sign = 1 if other[0] == "inc" else -1
                        reg[other[1]] += sign * reg[ctr[1]]
                        reg[ctr[1]] = 0
                        pc += 3
                        break
                else:
                    other = None
                if other is not None:
                    continue
        if op == "cpy":
            if ins[2] in reg:
                reg[ins[2]] = val(ins[1])
        elif op == "inc":
            if ins[1] in reg:
                reg[ins[1]] += 1
        elif op == "dec":
            if ins[1] in reg:
                reg[ins[1]] -= 1
        elif op == "jnz":
            if val(ins[1]) != 0:
                pc += val(ins[2])
                continue
        elif op == "tgl":
            t = pc + val(ins[1])
            if 0 <= t < len(prog):
                prog[t][0] = TOGGLE[prog[t][0]]
        pc += 1
    return reg["a"]


assert run(ipt_test, 0) == 3
print(run(ipt_puzzle, 7))
print(run(ipt_puzzle, 12))

# Part 1 solution: 10152
# Part 2 solution: 479006712
