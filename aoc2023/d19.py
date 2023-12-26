# coding: utf-8
import re

from boilerplate import read_input_file, run_func, test_func


def parse_ipt(ipt):
    # rfg{s<537:gd,x>2440:R,A}
    workflows = {}
    idx = 0
    while ipt[idx] != "":
        line = ipt[idx]
        ss = re.split(r"[{}]+", line)
        name = ss[0]
        rules_s = ss[1].split(",")
        rules = []
        for rule in rules_s:
            condition, destination = "", ""
            if ":" in rule:
                rr = rule.split(":")
                condition = rr[0]
                destination = rr[1]
            else:
                condition = "True"
                destination = rule
            rules.append((condition, destination))
        workflows[name] = rules
        idx += 1

    # {x=787,m=2655,a=1222,s=2876}
    parts = []

    idx += 1
    while idx < len(ipt):
        line = ipt[idx][1:-1]
        vars = {}
        for vv in line.split(","):
            kv = vv.split("=")
            vars[kv[0]] = int(kv[1])

        parts.append(vars)
        idx += 1

    return workflows, parts


def apply(workflow, part):

    wf = "in"
    variables = part

    while True:
        rules = workflow[wf]
        variables["ret"] = "CONT"
        for rule in rules:
            program = "if " + rule[0] + ": ret='" + rule[1] + "'"
            exec(program, variables)
            if variables["ret"] == "A":
                return sum([variables[z] for z in "xmas"])
            elif variables["ret"] == "R":
                return 0
            elif variables["ret"] == "CONT":
                pass
            else:
                wf = variables["ret"]
                break


def apply_intervals(workflow, DBG):

    ans = 0
    todo = [("in", (1, 4000), (1, 4000), (1, 4000), (1, 4000))]

    while len(todo) > 0:
        wf, r_x, r_m, r_a, r_s = todo[0]
        del todo[0]
        rules = workflow[wf]
        for rule in rules:

            cond = rule[0]
            dest = rule[1]

            (rpass_x, rpass_m, rpass_a, rpass_s) = (r_x, r_m, r_a, r_s)

            if cond == "True":
                if dest == "A":
                    ans += (
                        (r_x[1] - r_x[0] + 1)
                        * (r_m[1] - r_m[0] + 1)
                        * (r_a[1] - r_a[0] + 1)
                        * (r_s[1] - r_s[0] + 1)
                    )
                    if DBG:
                        print("A", r_x, r_m, r_a, r_s, ans)
                elif dest == "R":
                    if DBG:
                        print("R", r_x, r_m, r_a, r_s)
                else:
                    todo.append((rule[1], r_x, r_m, r_a, r_s))
            else:
                var = cond[0]
                cmp = cond[1]
                val = int(cond[2:])

                (rr_x, rr_m, rr_a, rr_s) = (r_x, r_m, r_a, r_s)

                if (var, cmp) == ("x", "<"):
                    rr_x = (r_x[0], val - 1)
                    rpass_x = (val, r_x[1])
                    pass
                elif (var, cmp) == ("x", ">"):
                    rr_x = (val + 1, r_x[1])
                    rpass_x = (r_x[0], val)
                    pass
                elif (var, cmp) == ("m", "<"):
                    rr_m = (r_m[0], val - 1)
                    rpass_m = (val, r_m[1])
                    pass
                elif (var, cmp) == ("m", ">"):
                    rr_m = (val + 1, r_m[1])
                    rpass_m = (r_m[0], val)
                    pass
                elif (var, cmp) == ("a", "<"):
                    rr_a = (r_a[0], val - 1)
                    rpass_a = (val, r_a[1])
                    pass
                elif (var, cmp) == ("a", ">"):
                    rr_a = (val + 1, r_a[1])
                    rpass_a = (r_a[0], val)
                    pass
                elif (var, cmp) == ("s", "<"):
                    rr_s = (r_s[0], val - 1)
                    rpass_s = (val, r_s[1])
                    pass
                elif (var, cmp) == ("s", ">"):
                    rr_s = (val + 1, r_s[1])
                    rpass_s = (r_s[0], val)
                    pass

                if dest == "A":
                    ans += (
                        (rr_x[1] - rr_x[0] + 1)
                        * (rr_m[1] - rr_m[0] + 1)
                        * (rr_a[1] - rr_a[0] + 1)
                        * (rr_s[1] - rr_s[0] + 1)
                    )
                    if DBG:
                        print("A", rr_x, rr_m, rr_a, rr_s, ans)
                elif dest == "R":
                    if DBG:
                        print("R", rr_x, rr_m, rr_a, rr_s)
                else:
                    todo.append((rule[1], rr_x, rr_m, rr_a, rr_s))
                (r_x, r_m, r_a, r_s) = (rpass_x, rpass_m, rpass_a, rpass_s)

    return ans


def boom_part1(ipt, DBG=True):
    workflows, parts = parse_ipt(ipt)

    ans = 0
    for part in parts:
        ans += apply(workflows, part)

    return ans


def boom_part2(ipt, DBG=True):
    workflows, _ = parse_ipt(ipt)

    ret = apply_intervals(workflows, DBG)

    return ret


# Test cases
#############


ipt_test1 = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".splitlines()
test_func(boom_part1, ipt_test1, 19114, True)
test_func(boom_part2, ipt_test1, 167409079868000, True)

# Real data
############

ipt_puzzle = read_input_file("input-d19.txt")

# part 1

result1 = run_func(boom_part1, ipt_puzzle, DBG=False)

# part 2

result2 = run_func(boom_part2, ipt_puzzle, DBG=False)

print("******")
print(f"# Part 1 solution: {result1}")
print(f"# Part 2 solution: {result2}")

quit()

# Part 1 solution: 331208
# Part 2 solution: 121464316215623
