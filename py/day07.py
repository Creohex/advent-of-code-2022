import re
from dataclasses import dataclass

@dataclass
class File:
    is_dir: bool
    name: str
    size: int
    contents: list

    def __init__(self, predicate, name, parent=None):
        self.is_dir = predicate == "dir"
        self.name = name
        self.size = None if self.is_dir else int(predicate)
        self.contents = []
        self.parent = parent
        self.path = f"{(self.parent.path + name + '/') if self.parent else name}"

    def __repr__(self) -> str:
        if self.is_dir:
            return f"<dir {self.name}: {self.contents} (size: {self.size})>"
        else:
            return f"<{self.name} {self.size}>"

    def __truediv__(self, name):
        return File("dir", name, parent=self)

    def __hash__(self):
        return self.path.__hash__()

    def visualize(self, level=0):
        result = (f"{'  ' * level}- {self.name} "
                  f"({'dir' if self.is_dir else f'file, size={self.size}'})")
        for _ in self.contents:
            result += f"\n{_.visualize(level + 1)}"
        return(result)

    def calculate_size(self):
        if self.size is None:
            self.size = sum(file.calculate_size() for file in self.contents)
        return self.size

@dataclass
class Cmd:
    command: str
    arg: str = None
    output: list[str] = None

    def __repr__(self):
        return f"{self.command} -> {self.arg if self.command == 'cd' else self.output}"

def parse_data() -> dict[str, File]:
    output = open("../inputs/day07", "r").read().strip().split("\n")
    pattern_cd = r"^\$\scd\s(.*)$"
    pattern_ls = r"^\$\sls$"
    pattern_contents = r"^(\d+|dir)\s([\w\.]+)$"
    commands = []
    i = 0

    while i < len(output):
        if m := re.match(pattern_cd, output[i]):
            commands.append(Cmd("cd", m.groups()[0], None))
        elif re.match(pattern_ls, output[i]):
            cmd_output = []
            j = i + 1
            while not output[j].startswith("$"):
                cmd_output.append(output[j])
                j += 1
                if j >= len(output):
                    break
            commands.append(Cmd("ls", output=cmd_output))
        i += 1

    fs = {"/": File("dir", "/")}
    cur_path = None

    for cmd in commands:
        if cmd.command == "cd":
            if cmd.arg == "/":
                cur_path = fs["/"].path
            elif cmd.arg == "..":
                cur_path = fs[cur_path].parent.path
            else:
                cur_path = (fs[cur_path] / cmd.arg).path
        elif cmd.command == "ls":
            for contents in cmd.output:
                predicate, name = re.match(pattern_contents, contents).groups()
                file = File(predicate, name, parent=fs[cur_path])
                if file.is_dir:
                    fs[file.path] = file
                fs[cur_path].contents.append(file)

    return fs


fs = parse_data()
[el.calculate_size() for el in fs.values()]
print(fs["/"].visualize())

# part 1
print(sum(filter(lambda size: size < 100000, map(lambda d: d.size, fs.values()))))

# part 2
print(min(filter(lambda s: s >= (fs["/"].size + 30_000_000 - 70_000_000),
                 map(lambda d: d.size, fs.values()))))
