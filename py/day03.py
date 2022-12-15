from functools import reduce

rucksacks = [_.strip() for _ in open("../inputs/day03", "r").readlines()]

def prio(item_type):
    if ord(item_type) < 97:
        return 27 + (ord(item_type) - ord("A"))
    else:
        return 1 + (ord(item_type) - ord("a"))

def part_one():
    return reduce(lambda acc, sack:
        acc + prio(set(sack[:len(sack)//2]).intersection(sack[len(sack)//2:]).pop()),
        rucksacks, 0)

def part_two():
    priority_sum = 0
    prev = 0
    for i in range(3, len(rucksacks) + 1, 3):
        a, b, c = rucksacks[prev:i]
        priority_sum += prio(set(a).intersection(b).intersection(c).pop())
        prev = i
    return priority_sum

print(part_one())
print(part_two())
