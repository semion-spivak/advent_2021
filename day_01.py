from operator import lt
from itertools import starmap, tee

with open('./input/day_01.txt', 'r') as f:
    data = list(map(int, f))

def sum_lt(i):
    a, b = tee(i, 2)
    next(b)
    return sum(starmap(lt, zip(a, b)))

if __name__ == '__main__':
    print(f'part 1: {sum_lt(data)}')
    print(f'part 2: {sum_lt(map(sum, zip(data[0:], data[1:], data[2:])))}')