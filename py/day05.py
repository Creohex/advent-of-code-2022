import re
from functools import reduce

def parse_input():
    raw = open("../inputs/day05", "r").read().strip().replace("[", "").replace("]", "")
    stacks_initial, commands_initial = raw.split("\n\n")
    stacks_initial = stacks_initial.split("\n")
    stacks = [[] for _ in range(len(stacks_initial[-1].split()))]
    stacks_initial = stacks_initial[:-1]
    for s in stacks_initial:
        s = s.replace("    ", "-").replace(" ", "")
        for i, crates in enumerate(s):
            for crate in crates:
                if crate != "-":
                    stacks[i].insert(0, crate)

    command_pattern = r"move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)"
    commands = []
    for command in commands_initial.split("\n"):
        commands.append(list(map(int, re.match(command_pattern, command).groups())))

    return stacks, commands

def operate_crane(multiple_crates_at_once=False):
    stacks, commands = parse_input()

    for amount, from_stack, to_stack in commands:
        if multiple_crates_at_once:
            stacks[to_stack - 1].extend(stacks[from_stack - 1][-amount:])
            stacks[from_stack - 1] = stacks[from_stack - 1][:-amount]
        else:
            for _ in range(amount):
                stacks[to_stack - 1].append(stacks[from_stack - 1].pop())

    return reduce(lambda acc, stack: acc + stack[-1], stacks, "")

print(operate_crane())
print(operate_crane(multiple_crates_at_once=True))
