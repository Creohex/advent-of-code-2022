
trees = list(map(list, open("../inputs/day08", "r").read().strip().split("\n")))
visible = 0
most_scenic = 0

for y in range(1, len(trees) - 1):
    for x in range(1, len(trees[0]) - 1):
        scenic_score = 1
        open_directions = 4
        height = trees[y][x]

        for j in reversed(range(0, y)):
            if trees[j][x] >= height:
                open_directions -= 1
                break
        scenic_score *= y - j

        for j in range(y + 1, len(trees)):
            if trees[j][x] >= height:
                open_directions -= 1
                break
        scenic_score *= j - y

        for i in reversed(range(0, x)):
            if trees[y][i] >= height:
                open_directions -= 1
                break
        scenic_score *= x - i

        for i in range(x + 1, len(trees[0])):
            if trees[y][i] >= height:
                open_directions -= 1
                break
        scenic_score *= i - x

        if open_directions:
            visible += 1
        most_scenic = max(most_scenic, scenic_score)


print(visible + len(trees) * 2 + len(trees[0]) * 2 - 4)  # part 1
print(most_scenic)                                       # part 2
