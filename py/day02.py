from functools import reduce

guide = [signs.replace("X", "A").replace("Y", "B").replace("Z", "C").split()
         for signs in open("../inputs/day02")]
wins = {"A": "C", "B": "A", "C": "B"}
wins_rev = {v: k for k,v in wins.items()}
weights = {"A": 1, "B": 2, "C": 3}

def play(me, oppo):
    return weights[me] + (3 if me == oppo else 6 if wins[me] == oppo else 0)

print(reduce(lambda acc, l: acc + play(l[1], l[0]), guide, 0))                 # part 1
print(reduce(lambda acc, l: acc + play(wins[l[0]] if l[1] == "A"
                                       else l[0] if l[1] == "B"
                                       else wins_rev[l[0]], l[0]), guide, 0))  # part 2
