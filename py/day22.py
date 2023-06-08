import re

raw = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


class Board:
    def __init__(self, content) -> None:
        raw, actions = content.split("\n\n")
        raw = raw.split("\n")
        self.width = 0
        self.height = len(raw)
        self.coords = {}
        self.start_pos = None
        self.actions = [
            v if v in "LR" else int(v) for v in re.findall(r"([RL]|\d+)", actions)
        ]

        for y in range(len(raw)):
            for x in range(len(raw[y])):
                if raw[y][x] != " ":
                    if not self.start_pos and raw[y][x] == ".":
                        self.start_pos = (x, y)
                    self.coords[(x, y)] = raw[y][x]
                    self.width = max(self.width, x + 1)

    def draw(self, coords=None, path=None, pos=None):
        coords = coords or self.coords
        lines = [[] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                lines[y].append(coords.get((x, y), " "))

        if path:
            for (x, y), icon in path.items():
                lines[y][x] = icon
        if pos:
            lines[pos[1]][pos[0]] = "x"

        print("\n".join("".join(line) for line in lines))

    def traverse(self, fold=False, size=50):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dir_signs = {dirs[0]: ">", dirs[1]: "v", dirs[2]: "<", dirs[3]: "^"}
        dir = dirs[0]
        path = {}
        x, y = self.start_pos
        coord_keys = list(self.coords)

        # TODO: derive cube side relations automatically?
        # (x, y) outbounds -> (wrapped_x, wrapped_y, new_direction)
        wraps = {}

        if fold:
            for dx in range(size):
                # Example mapping
                # # 1
                # side_coords[(8 + offset, -1)] = (3 - offset, 4), dirs[1]
                # side_coords[(7, offset)] = (4 + offset, 4), dirs[3]
                # side_coords[(12, offset)] = (15, 11 - offset), dirs[2]
                # # 2
                # side_coords[(offset, 3)] = (11 - offset, 0), dirs[1]
                # side_coords[(offset, 8)] = (11 - offset, 11), dirs[3]
                # side_coords[(-1, 4 + offset)] = (12 + offset, 11), dirs[3]
                # # 3
                # side_coords[(4 + offset, 3)] = (8, offset), dirs[0]
                # side_coords[(4 + offset, 8)] = (8, 11 - offset), dirs[0]
                # # 4
                # side_coords[(12, 4 + offset)] = (15 - offset, 8), dirs[1]
                # # 5
                # side_coords[(7, 8 + offset)] = (4 + offset, 7), dirs[3]
                # side_coords[(8 + offset, 12)] = (3 - offset, 7), dirs[3]
                # # 6
                # side_coords[(12 + offset, 7)] = (11, 7 - offset), dirs[2]
                # side_coords[(12 + offset, 12)] = (0, 7 - offset), dirs[0]
                # side_coords[(16, 8 + offset)] = (11, 3 - offset), dirs[2]

                # Puzzle mapping
                # side 1:
                wraps[(size + dx, -1)] = (0, 3 * size + dx), dirs[0]
                wraps[(size - 1, dx)] = (0, 3 * size - 1 - dx), dirs[0]

                # side 2:
                wraps[(2 * size + dx, -1)] = (dx, 4 * size - 1), dirs[3]
                wraps[(3 * size, dx)] = (2 * size - 1, 3 * size - 1 - dx), dirs[2]
                wraps[(2 * size + dx, size)] = (2 * size - 1, size + dx), dirs[2]

                # side 3:
                wraps[(size - 1, size + dx)] = (dx, 2 * size), dirs[1]
                wraps[(2 * size, size + dx)] = (2 * size + dx, size - 1), dirs[3]

                # side 4:
                wraps[(dx, 2 * size - 1)] = (size, size + dx), dirs[0]
                wraps[(-1, 2 * size + dx)] = (size, size - 1 - dx), dirs[0]

                # side 5:
                wraps[(2 * size, 2 * size + dx)] = (3 * size - 1, size - 1 - dx), dirs[2]
                wraps[(size + dx, 3 * size)] = (size - 1, 3 * size + dx), dirs[2]

                # side 6:
                wraps[(-1, 3 * size + dx)] = (size + dx, 0), dirs[1]
                wraps[(size, 3 * size + dx)] = (size + dx, 3 * size - 1), dirs[3]
                wraps[(dx, 4 * size)] = (2 * size + dx, 0), dirs[1]

        for action in self.actions:
            if isinstance(action, int):
                for _ in range(action):
                    nx, ny = x + dir[0], y + dir[1]
                    new_dir = dir
                    if not self.coords.get((nx, ny)):
                        if fold:
                            (nx, ny), new_dir = wraps[(nx, ny)]
                        else:
                            match dirs.index(dir):
                                case 0:
                                    nx = min(x for x, y in coord_keys if y == ny)
                                case 1:
                                    ny = min(y for x, y in coord_keys if x == nx)
                                case 2:
                                    nx = max(x for x, y in coord_keys if y == ny)
                                case 3:
                                    ny = max(y for x, y in coord_keys if x == nx)
                    match self.coords[nx, ny]:
                        case ".":
                            path[x, y] = dir_signs[dir]
                            x, y = nx, ny
                            dir = new_dir
                        case "#":
                            break
            else:
                dir = dirs[(dirs.index(dir) + (1 if action == "R" else -1)) % len(dirs)]

            # self.draw(path=path, pos=(x, y))
        return 1000 * (y + 1) + 4 * (x + 1) + dirs.index(dir)


with open("../inputs/day22", "r") as f:
    board = Board(f.read().rstrip())

print(f"part 1: {board.traverse()}")
print(f"part 2: {board.traverse(fold=True)}")
