import re


def parse_input():
    cmd_pattern = r"^(noop|addx)\s?(\-?\d+)?$"
    instructions = []
    for line in open("../inputs/day10", "r").read().strip().split("\n"):
        instruction, val = re.match(cmd_pattern, line).groups()
        instructions.append((instruction, int(val) if val else None))
    return instructions


noop = lambda *args: None
addx = lambda context, val: context.update({"x": context["x"] + val})
actions = {
    "noop": [noop],
    "addx": [noop, addx],
}

context = {"x": 1}
signal_strength_total = 0
cycle = 0
monitor_width = 40
monitor = [" "] * monitor_width * 6
interesting_cycles = [20, 60, 100, 140, 180, 220]

for instruction, val in parse_input():
    for action in actions[instruction]:
        cycle += 1

        if cycle in interesting_cycles:
            signal_strength = cycle * context["x"]
            signal_strength_total += signal_strength

        if abs(context["x"] + 1 - cycle % monitor_width) < 2:
            monitor[cycle - 1] = "#"

        action(context, val)

print(signal_strength_total)                      # part 1
for i in range(0, 240, monitor_width):
    print("".join(monitor[i:i + monitor_width]))  # part 2
