with open('./input/day_06.txt', 'r') as f:
    school = [(1, x) for x in map(int, f.read().strip('\n').split(','))]

def run(n):
    for _ in range(n):
        new_fish = 0
        for i, (amount, age) in enumerate(school):
            age -= 1
            if age < 0:
                age = 6
                new_fish += amount
            school[i] = (amount, age)
        if new_fish:
            school.append((new_fish, 8))
    return sum(map(lambda x: x[0], school))


if __name__ == '__main__':
    print(f'part 1: {run(80)}')
    print(f'part 2: {run(256-80)}')
