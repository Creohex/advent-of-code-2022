def parse_input():
    m = []
    start = (0, 0)
    finish = (0, 0)

    for line in open("../inputs/day12", "r").read().strip().split("\n"):
        m.append(list(line))
        y = len(m) - 1
        try:
            start = (m[-1].index("S"), y)
            m[-1][start[0]] = "a"
        except ValueError:
            pass
        try:
            finish = (m[-1].index("E"), y)
            m[-1][finish[0]] = "z"
        except ValueError:
            pass

    md = {(x,y): ord(m[y][x]) for y in range(len(m)) for x in range(len(m[y]))}
    return md, start, finish

def visualize(m, pos=None, target=None, steps=None):
    rep = [["." for w in range(max(map(lambda p: p[0], m)) + 1)]
           for h in range(max(map(lambda p: p[1], m)) + 1)]
    for k, v in m.items():
        x, y = k
        rep[y][x] = "S" if k == pos else "E" if k == target else  "." if steps else chr(v)
    for k in steps or {}:
        rep[k[1]][k[0]] = chr(m[k])
    for y in rep:
        print("".join(y))

def traverse(hill_map, start, finish, show=False):
    directions = ((0, -1), (1, 0), (-1, 0), (0, 1))
    paths = [[start]]
    visited = [start]
    depth = 0

    while True:
        new_paths = []

        for path in paths:
            if len(path) <= depth:
                continue
            pos = path[-1]
            neighbours = []

            for dx, dy in directions:
                neighbour_pos = pos[0] + dx, pos[1] + dy
                elevation = hill_map.get(neighbour_pos)
                if (elevation
                    and neighbour_pos not in visited
                    and elevation - hill_map[pos] <= 1
                ):
                    if neighbour_pos == finish:
                        if show:
                            visualize(hill_map, start, finish,
                                      steps={_: hill_map[_] for _ in path})
                        return len(path)
                    neighbours.append(neighbour_pos)

            if not neighbours:
                continue
            path.append(neighbours[0])
            for neighbour in neighbours[1:]:
                path = list(path)
                path[-1] = neighbour
                new_paths.append(path)
            visited.extend(neighbours)
        paths.extend(new_paths)
        depth += 1

        paths = [path for path in paths if len(path) >= depth - 1]
        if not paths:
            return None  # Unreachable


hill_map, start, finish = parse_input()

# part 1:
print(traverse(hill_map, start, finish, show=True))

# part 2:
print(min(filter(bool, map(lambda pos: traverse(hill_map, pos, finish),
                           filter(lambda p: hill_map[p] == ord("a"), hill_map)))))
