snafu = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}
snafu_rev = {v: k for k, v in snafu.items()}
ranks = [(5 ** r, [d * 5 ** r for d in snafu.values()]) for r in range(22)]

def snafu_to_decimal(val: str) -> int:
    return sum(snafu[v] * 5 ** i for i, v in enumerate(reversed(val)))

def decimal_to_snafu(val: int) -> str:
    res = ""

    for rank, dev in ranks:
        for d in dev:
            new_val = val - d
            next_rank = rank * 5
            if not (new_val % next_rank):
                res += snafu_rev[d // rank]
                if not new_val:
                    return "".join(reversed(res))
                val = new_val
                break

print(decimal_to_snafu(sum(map(snafu_to_decimal,
                               open("../inputs/day25", "r").read().strip().split("\n")))))
