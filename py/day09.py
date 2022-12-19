import re


def parse_input():
    motion_pattern = r"^([UDLR])\s(\d+)$"
    instructions = []
    for line in open("../inputs/day09", "r").read().strip().split("\n"):
        heading, steps = re.match(motion_pattern, line.strip()).groups()
        instructions.append((heading, int(steps)))
    return instructions

def visualize(nodes, extras=None):
    nodes = list(nodes)
    extras = extras or []
    x_coords, y_coords = (set(map(lambda node: node[axis], nodes + extras))
                          for axis in range(2))
    pad_right, pad_up = (abs(min(coords)) for coords in (x_coords, y_coords))
    width = max(x_coords) + pad_right + 1
    height = max(y_coords) + pad_up + 1
    output = [list(" " * width) for _ in range(height)]
    for x, y in nodes:
        output[y + pad_up][x + pad_right] = "#"
    extra_knots = ''.join(map(str, range(1, len(extras) - 2)))
    for coords, name in reversed(list(zip(extras, f"H{extra_knots}Ts"))):
        output[coords[1] + pad_up][coords[0] + pad_right] = name
    for line in reversed(range(len(output))):
        print("".join(output[line]))

def simulate(knots=2):
    moves = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }
    knots = [(0, 0) for _ in range(knots)]
    tail_log = set([knots[-1]])

    for heading, steps in parse_input():
        move = moves[heading]
        for _ in range(steps):
            head = knots[0]
            knots[0] = head[0] + move[0], head[1] + move[1]
            for i in range(1, len(knots)):
                rel_head = knots[i - 1]
                knot = knots[i]
                diff = sum(abs(rel_head[axis] - knot[axis]) for axis in range(2))
                if diff > 2:
                    knots[i] = (knot[0] + (1 if rel_head[0] > knot[0] else -1),
                                knot[1] + (1 if rel_head[1] > knot[1] else -1))
                elif diff == 2:
                    if rel_head[0] == knot[0]:
                        knots[i] = knot[0], knot[1] + (1 if rel_head[1] > knot[1] else -1)
                    elif rel_head[1] == knot[1]:
                        knots[i] = knot[0] + (1 if rel_head[0] > knot[0] else -1), knot[1]
            tail_log.add(knots[-1])
        # visualize(tail_log, extras=knots)

    # visualize(tail_log)
    return len(set(tail_log))


print(simulate())          # part 1
print(simulate(knots=10))  # part 2
