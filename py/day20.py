from collections import deque

with open("../inputs/day20") as f:
    sequence = deque(enumerate([int(_) for _ in f.read().strip().split("\n")]))
# sequence = deque(enumerate([1, 2, -3, 3, -2, 0, 4]))


def move(seq: deque, idx: int = 0):
    while seq[0][0] != idx:
        seq.rotate()
    (_, hops) = seq.popleft()
    seq.rotate(-hops)
    seq.appendleft((idx, hops))


def mix(seq: list):
    [move(seq, i) for i in range(len(seq))]


def solve(multiplicator: int = 1, mixes: int = 1):
    seq = deque((idx, val * multiplicator) for idx, val in sequence)
    [mix(seq) for _ in range(mixes)]

    while seq[0][1] != 0:
        seq.rotate()
    return sum(seq[nth % len(seq)][1] for nth in (1000, 2000, 3000))


print(f"part 1: {solve()}")
print(f"part 2: {solve(multiplicator=811589153, mixes=10)}")
