from collections import deque

def visualize(elves):
    elves_x = list(map(lambda e: e[0], elves))
    elves_y = list(map(lambda e: e[1], elves))
    s, n, w, e = min(elves_y), max(elves_y), min(elves_x), max(elves_x)
    lines = [["." for x in range(e - w + 1)] for y in range(n - s + 1)]
    for x, y in elves:
        lines[y - s][x - w] = "#"
    [print("".join(line)) for line in lines]
    print("Empty spots: ", (e - w + 1) * (n - s + 1) - len(elves))


lines = open("../inputs/day23", "r").read().strip().split("\n")
elves = [(x, y)
        for y in range(len(lines))
        for x in range(len(lines[0]))
        if lines[y][x] == "#"]
neighbours = ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (-1, -1), (1, 1))
directions = [
    ((0, -1), [(-1, -1), (0, -1), (1, -1)]),  # N
    ((0, 1), [(-1, 1), (0, 1), (1, 1)]),      # S
    ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),  # W
    ((1, 0), [(1, -1), (1, 0), (1, 1)]),      # E
]
directions_order = deque(range(len(directions)))
round = 1

while True:
    print("~", end="", flush=True)
    moves = {}
    elves_moved = False

    for elf in elves:
        x, y = elf
        if not any((x + dx, y + dy) in elves for dx, dy in neighbours):
            moves[elf] = moves[elf] + [elf] if moves.get(elf) else [elf]
            continue
        for ith_dir in directions_order:
            direction, check_directions = directions[ith_dir]
            if all((x + dx, y + dy) not in elves for dx, dy in check_directions):
                m = (x + direction[0], y + direction[1])
                moves[m] = moves[m] + [elf] if moves.get(m) else [elf]
                elves_moved = True
                break
        else:
            moves[elf] = moves[elf] + [elf] if moves.get(elf) else [elf]

    elves_new = []
    for coord, elves_to_move in moves.items():
        if len(elves_to_move) == 1:
            elves_new.append(coord)
        else:
            elves_new.extend(elves_to_move)
    elves = elves_new

    if round == 10:
        print("\nPart 1: (round 10)")
        visualize(elves)
    if not elves_moved:
        print("\nPart 2:", round)
        break

    directions_order.rotate(-1)
    round += 1
