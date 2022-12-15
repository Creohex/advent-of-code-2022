
import re

pattern = r"(\d+)-(\d+),(\d+)-(\d+)"
ranges = [list(map(int, re.match(pattern, _).groups()))
          for _ in open("../inputs/day04", "r")]

print(len(list(filter(
    lambda r: r[0] >= r[2] and r[1] <= r[3] or r[0] <= r[2] and r[1] >= r[3],
    ranges))))  # part 1

print(len(list(filter(
    lambda r: (r[1] >= r[2] and r[0] <= r[2]
               or r[0] <= r[3] and r[1] >= r[3]
               or r[0] >= r[2] and r[1] <= r[3]
               or r[2] <= r[0] and r[3] >= r[1]),
    ranges))))  # part 2
