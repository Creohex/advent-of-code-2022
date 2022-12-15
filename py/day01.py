
calories = []
with open("../inputs/day01", "r") as f:
    for cals in f.read().split("\n\n"):
        calories.append(sum(map(int, cals.strip().split("\n"))))
calories.sort()

print(calories[-1])         # part_one
print(sum(calories[-3:]))   # part_two
