# coding: utf-8
import operator
import string
import time

# used this implementation, with reversed precedence of * and +
# https://codereview.stackexchange.com/a/46702


class Operator(object):
    def __init__(self, op, precedence):
        self._op = op
        self._prec = precedence

    def __call__(self, *args):
        return self._op(*args)

    def __lt__(self, op):
        return self._prec < op._prec

    def __gt__(self, op):
        return self._prec > op._prec

    def __eq__(self, op):
        return self._prec == op._prec

    def __repr__(self):
        return repr(self._op)

    def __str__(self):
        return str(self._op)


class Calculator(object):
    operators = {
        "*": Operator(operator.mul, 1),
        "+": Operator(operator.add, 2),
    }

    def __init__(self):
        pass

    def calculate(self, expr):
        tokens = self.parse(expr)
        result = self.evaluate(tokens)
        return result

    def evaluate(self, tokens, trace=False):
        stack = []
        for item in tokens:
            if isinstance(item, Operator):
                if trace:
                    print(stack)

                b, a = int(stack.pop()), int(stack.pop())
                result = item(a, b)
                stack.append(result)

                if trace:
                    print(stack)
            else:  # anything else just goes on the stack
                stack.append(item)

        return stack[0]

    def parse(self, expr, trace=False):
        tokens = []
        op_stack = []

        last = None

        for c in expr:
            if c in string.whitespace:
                last = c
            elif c in string.digits:
                value = str(c)
                if last and last in string.digits:  # number continues, just append it
                    value = tokens.pop() + value

                last = c
                tokens.append(value)
            elif c == "(":
                op_stack.append("(")
            elif c == ")":
                # closing parens found, unwind back to the matching open
                while op_stack:
                    curr = op_stack.pop()
                    if curr == "(":
                        break
                    else:
                        tokens.append(curr)
            else:  # not a number or a parens, must be an operator
                op = self.operators.get(c, None)
                while op_stack:
                    curr = op_stack[-1]
                    # the 'is' check prevents comparing an Operator to a string
                    if curr == "(":  # don't leave the current scope
                        break
                    elif curr < op:
                        break
                    tokens.append(op_stack.pop())

                op_stack.append(op)
                last = c

        while op_stack:
            op = op_stack.pop()
            tokens.append(op)

        return tokens


def boom(input_val, DBG=True):
    calc = Calculator()
    ret = 0
    for expr in input_val:
        # value = calculate(expr, DBG)
        value = calc.calculate(expr)
        ret = ret + value

    return ret


def test(cc=None, expected=None, DBG=False):
    start_millis = int(round(time.time() * 1000))
    result = boom(cc, DBG)
    stop_millis = int(round(time.time() * 1000))
    result = str(result)
    expected = str(expected)
    flag = result == expected
    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + str(flag)
            + " -> expected "
            + expected
        )
    print(
        (stop_millis - start_millis),
        "ms",
        int((stop_millis - start_millis) / 1000),
        "s",
        int((stop_millis - start_millis) / 1000 / 60),
        "min",
    )
    return flag


t1 = """1 + 2 * 3 + 4 * 5 + 6"""
tt1 = t1.splitlines()
test(tt1, 231, True)
# sys.exit()

t1 = """1 + (2 * 3) + (4 * (5 + 6))"""
tt1 = t1.splitlines()
test(tt1, 51, True)
# sys.exit()

t1 = """2 * 3 + (4 * 5)"""
tt1 = t1.splitlines()
test(tt1, 46, True)
# sys.exit()
t1 = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""
tt1 = t1.splitlines()
test(tt1, 1445, True)
# sys.exit()
t1 = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
tt1 = t1.splitlines()
test(tt1, 669060, True)
# sys.exit()
t1 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
tt1 = t1.splitlines()
test(tt1, 23340, True)
# sys.exit()

INPUT_FILE = "input-d18.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

ret = boom(puzzle_input, DBG=True)
print(ret)

# part 2 = 20394514442037
