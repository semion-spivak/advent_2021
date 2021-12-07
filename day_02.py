class Submarine:
    def __init__(self, commands):
        self.commands = commands
        self.x, self.y = 0, 0

    def down(self, y):
        self.y += y

    def forward(self, x):
        self.x += x

    def up(self, y):
        self.y -= y
        if self.y < 0:
            self.y = 0

    def get_final_pos(self):
        for c, param in self.commands:
            getattr(self, c)(param)
        return self.x * self.y


class SubmarineV2(Submarine):
    def __init__(self, *args):
        super().__init__(*args)
        self.aim = 0

    def down(self, y):
        self.aim += y

    def up(self, y):
        self.aim -= y

    def forward(self, x):
        self.x += x
        self.y += self.aim * x
        if self.y < 0:
            self.y = 0


with open('./input/day_02.txt', 'r') as f:
    commands = []
    for line in f:
        c, param = line.strip('\n').split(' ')
        commands.append((c, int(param)))

if __name__ == '__main__':
    print(f'part 1: {Submarine(commands).get_final_pos()}')
    print(f'part 2: {SubmarineV2(commands).get_final_pos()}')
