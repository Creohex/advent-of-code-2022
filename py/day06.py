def subroutine(unique=None):
    sequence = open("../inputs/day06", "r").read().strip()
    buff = list(sequence[:unique - 1])
    for i in range(unique - 1, len(sequence)):
        buff.append(sequence[i])
        if len(buff) > unique:
            buff.pop(0)
        if len(set(buff)) == unique:
            return i + 1

print(subroutine(unique=4))   # part 1
print(subroutine(unique=14))  # part 2
