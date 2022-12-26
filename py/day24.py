from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Blizzard:
    x: int
    y: int
    direction: tuple[int, int]

    directions_map = {
        (1, 0): ">",
        (-1, 0): "<",
        (0, -1): "^",
        (0, 1): "v",
    }
    directions_map_rev = {v: k for k,v in directions_map.items()}

    @property
    def img(self):
        return self.directions_map[self.direction]

    @property
    def coords(self):
        return self.x, self.y

    def project_position(self, time, width, height) -> Blizzard:
        return Blizzard(((self.x + self.direction[0] * time - 1) % (width - 2)) + 1,
                        ((self.y + self.direction[1] * time - 1) % (height - 2)) + 1,
                        self.direction)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.img})"

    def __hash__(self):
        return (self.x << 16) + self.y


lines = open("../inputs/day24", "r").read().strip().split("\n")
blizzards = [Blizzard(x, y, Blizzard.directions_map_rev[lines[y][x]])
             for y in range(len(lines))
             for x in range(len(lines[y]))
             if lines[y][x] in Blizzard.directions_map_rev]
x_blizzards = {}
y_blizzards = {}
for b in blizzards:
    if b.direction[0]:
        x_blizzards[b.y] = x_blizzards[b.y] + [b] if x_blizzards.get(b.y) else [b]
    else:
        y_blizzards[b.x] = y_blizzards[b.x] + [b] if y_blizzards.get(b.x) else [b]
width = len(lines[0])
height = len(lines)
start = (1, 0)
finish = (width - 2, height - 1)


def visualize(time=0, current_pos=None, path=None) -> None:
    lines = [["#"] + ["."] * (width - 2) + ["#"]
             for _ in range(height)]
    lines[0] = ["#", "."] + ["#"] * (width - 2)
    lines[-1] = list(reversed(lines[0]))
    entities = {}

    if path:
        for x, y in path:
            lines[y][x] = "@"
    else:
        for b in [_.project_position(time, width, height) for _ in blizzards]:
            entity = entities.get(b.coords)
            if not entity:
                entities[b.coords] = b.img
            elif isinstance(entity, int):
                entities[b.coords] += 1
            else:
                entities[b.coords] = 2
        if current_pos:
            entities[current_pos] = "X"
        for (x, y), v in entities.items():
            lines[y][x] = str(v)

    [print("".join(line)) for line in lines]


def intersects(x, y, time) -> bool:
    if x_blizz := x_blizzards.get(y):
        if x in [b.project_position(time, width, height).x for b in x_blizz]:
            return True
    if y_blizz := y_blizzards.get(x):
        if y in [b.project_position(time, width, height).y for b in y_blizz]:
            return True
    return False


def traverse(pos_from, pos_to, time=0) -> int:
    possible_moves = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    paths = [[pos_from]]

    while True:
        time += 1
        new_paths = []

        for path in paths:
            x, y = path[-1]
            next_moves = []

            for next_move in ((x + dx, y + dy) for dx, dy in possible_moves):
                mx, my = next_move
                if ((0 < mx < width - 1 and 0 < my < height - 1
                     or mx == 1 and my == 0                    # entrance
                     or mx == width - 2 and my == height - 1)  # exit
                    and not intersects(mx, my, time)
                ):
                    next_moves.append(next_move)
                    if (mx, my) == pos_to:
                        print(f"\n{pos_from} -> {pos_to}:")
                        visualize(path=path + [(mx, my)])
                        return time
            [new_paths.append(path + [next_move]) for next_move in next_moves]

        paths = new_paths
        remove_path_ids = set()
        unique_coords = set()

        for path_idx, path in enumerate(paths):
            if path[-1] in unique_coords:
                remove_path_ids.add(path_idx)
            else:
                unique_coords.add(path[-1])
        for idx in sorted(remove_path_ids, reverse=True):
            del paths[idx]
        if not paths:
            raise Exception("Path not found!")


def traverse_multiple(points_of_interst) -> int:
    time = 0
    for a, b in zip(points_of_interst, points_of_interst[1:]):
        time = traverse(a, b, time=time) + 1
    return time - 1


print("Part 1: ", traverse(start, finish))
print("Part 2: ", traverse_multiple([start, finish, start, finish]))
