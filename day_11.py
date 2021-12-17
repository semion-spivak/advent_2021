from io import StringIO
from copy import copy

adj = ((-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1))

max_y, max_x = 0, 0
def load(f):
    global max_y, max_x
    data = dict()
    for y, line in enumerate(f):
        max_y = max(max_y, y)
        for x, energy in enumerate(map(int, line.strip('\n'))):
            data[(y, x)] = energy
            max_x = max(max_x, x)
    return data


def flash(data, flashed, y, x):
    for dy, dx in adj:
        if x+dx < 0 or x+dx > max_x or y+dy < 0 or y+dy > max_y:
            continue
        incr_energy(data, flashed, (y+dy, x+dx))

def incr_energy(data, flashed, yx):
    data[yx] += 1
    if data[yx] > 9:
        if yx not in flashed:
            flashed.add(yx)
            flash(data, flashed, *yx)


def print_data(data):
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(data[(y, x)], end='')
        print()

def step(data):
    """
    >>> data = load(StringIO(\
    '11111\\n'\
    '19991\\n'\
    '19191\\n'\
    '19991\\n'\
    '11111'))
    >>> step(data)
    >>> print_data(data)
    34543
    40004
    50005
    40004
    34543
    >>> step(data)
    >>> print_data(data)
    45654
    51115
    61116
    51115
    45654
    """
    flashed = set()
    for yx in data.keys():
        incr_energy(data, flashed, yx)
    for yx in flashed:
        data[yx] = 0
    return len(flashed)

def part_1(data):
    """
    >>> data = load(StringIO(\
    '5483143223\\n' \
    '2745854711\\n' \
    '5264556173\\n' \
    '6141336146\\n' \
    '6357385478\\n' \
    '4167524645\\n' \
    '2176841721\\n' \
    '6882881134\\n' \
    '4846848554\\n' \
    '5283751526'))
    >>> part_1(data)
    1656
    """
    return sum([step(data) for _ in range(100)])

def part_2(data):
    i = 0
    while True:
        c = step(data)
        i += 1
        if c == len(data):
            return i

if __name__ == '__main__':
    with open('./input/day_11.txt', 'r') as f:
        data = load(f)
    print(f'part 1: {part_1(copy(data))}')
    print(f'part 2: {part_2(data)}')