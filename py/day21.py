import operator
import re


raw = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def parse_input(text):
    pattern = r"^([a-z]{4}): (?:(?:([a-z]{4}) ([\+\-\*\/]){1} ([a-z]{4}))|(\d+))$"
    monkeys = {}
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    for line in text.strip().split("\n"):
        grp = re.search(pattern, line).groups()
        if grp[-1]:
            monkeys[grp[0]] = int(grp[-1])
        else:
            monkeys[grp[0]] = (grp[1], grp[3], operators[grp[2]])

    return monkeys


monkeys = parse_input(raw)
# with open("../inputs/day21") as f:
#     monkeys = parse_input(f.read())


def unfold(name):
    if isinstance(monkeys[name], int):
        return monkeys[name]
    arg1, arg2, op = monkeys[name]
    return int(op(unfold(arg1), unfold(arg2)))


def unfold_hum(name):
    if isinstance(monkeys[name], int):
        return monkeys[name], name == "humn"
    name1, name2, op = monkeys[name]
    val1, humn1 = unfold_hum(name1)
    val2, humn2 = unfold_hum(name2)
    return int(op(val1, val2)), humn1 or humn2


# TODO: fix
def equate() -> int:
    name1, name2, _ = monkeys["root"]
    val1, is_humn = unfold_hum(name1)
    val2, _ = unfold_hum(name2)
    val = val1 if not is_humn else val2
    # print(val)

    def search(name):
        # print("Searching: ", name)
        for m in monkeys:
            if isinstance(monkeys[m], tuple):
                if monkeys[m][0] == name:
                    return m, monkeys[m][2], unfold(monkeys[m][1]), False
                elif monkeys[m][1] == name:
                    return m, monkeys[m][2], unfold(monkeys[m][0]), True

    stop = name1 if is_humn else name2

    def build_stack(name):
        reverse_op = {
            operator.add: operator.sub,
            operator.sub: operator.add,
            operator.mul: operator.truediv,
            operator.truediv: operator.mul,
        }
        stack = []
        while True:
            if name == stop:
                break
            n, op, val, is_left = search(name)
            stack.insert(0, (reverse_op[op], val, is_left))
            name = n
        return stack

    for op, v, is_left in build_stack("humn"):
        args = (val, v) if is_left else (v, val)
        val = int(op(*args))
        # print(val)

    return val

print(f"part 1: {unfold('root')}")
print(f"part 2: {equate()}")
