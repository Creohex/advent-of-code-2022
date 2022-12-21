
import re
from dataclasses import dataclass
from operator import __add__, __mul__

raw = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass
class Monkey:
    _id: int
    items: list[int]
    _second_arg: str | int
    worry_method: callable
    test_div_value: int
    on_success: int
    on_fail: int
    inspected: int = 0

    def __repr__(self):
        return f"Monkey {self._id}: inspected {self.inspected}"

    @property
    def second_arg(self):
        return None if self._second_arg == "old" else self._second_arg


@dataclass
class Item:
    val: int
    rem: int
    rems: dict[int, int]

    def __repr__(self):
        return str(self.val)


def parse_input():
    monkeys = []
    pattern = (
        r"(?sm)"                                                     # set multiline
        r"^Monkey\s(\d+):$\n"                                        # name
        r"^\s+Starting\sitems:\s(.*)$\n"                             # items
        r"^\s+Operation:\snew\s=\sold\s(\+|\*)\s(old|\d+)$\n"        # formula
        r"^\s+Test:\sdivisible\sby\s(\d+)$\n"                        # test case
        r"^\s+If\strue:\sthrow\sto\smonkey\s(\d+)$\n"                # test passes
        r"^\s+If\sfalse:\sthrow\sto\smonkey\s(\d+)$")                # test fails

    # for monkey in raw.strip().split("\n\n"):
    for monkey in open("../inputs/day11", "r").read().strip().split("\n\n"):
        data = re.match(pattern, monkey).groups()
        _id, items, op_operator, arg2, test, succeeds, fails = data

        monkeys.append(Monkey(_id=int(_id),
                              items=list(map(lambda i: Item(i, i % int(test), dict()),
                                             map(int, items.split(", ")))),
                              _second_arg=arg2 if arg2 == "old" else int(arg2),
                              worry_method=__mul__ if op_operator == "*" else __add__,
                              test_div_value=int(test),
                              on_success=int(succeeds),
                              on_fail=int(fails)))

    for rem in map(lambda m: m.test_div_value, monkeys):
        for m in monkeys:
            for i in m.items:
                i.rems[rem] = i.val % rem

    return monkeys

def shenanigans(rounds, optimized=False):
    monkeys = parse_input()

    for _ in range(rounds):
        for m in monkeys:
            while m.items:
                item = m.items.pop(0)
                if not optimized:
                    item.val = m.worry_method(item.val, m.second_arg or item.val) // 3
                    item.rem = item.val % m.test_div_value
                else:
                    # FIXME: ...
                    r = item.rems[m.test_div_value]
                    item.rem = m.worry_method(r, m.second_arg or r)
                    for div in item.rems:
                        item.rems[div] = item.rem % div
                target_monkey_id = m.on_fail if item.rem else m.on_success
                monkeys[target_monkey_id].items.append(item)
                m.inspected += 1
        # print(f"\nRound: {_ + 1}")
        # [print(_) for _ in monkeys]
    print((insp := sorted(map(lambda m: m.inspected, monkeys)))[-1] * insp[-2])


shenanigans(20)                     # part 1
shenanigans(10000, optimized=True)  # part 2
