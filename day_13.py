from io import StringIO
import numpy as np
import re


def load(f):
    coords = []

    while (line := f.readline()) != '\n':
        x, y = tuple(map(int, line.split(',')))
        coords.append((x, y))
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    a = np.zeros((max_x+1, max_y+1), dtype=int) == 1
    for x, y in coords:
        a[x, y] = True

    folding_instructions = []
    for line in f:
        m = re.match(r'fold along (?P<axis>x|y)=(?P<at_coord>\d+)', line).groupdict()
        m['at_coord'] = int(m['at_coord'])
        folding_instructions.append(m)
    return a, folding_instructions

def print_dots(a, space=' '):
    _x, _y = a.shape
    for y in range(_y):
        for x in range(_x):
            print('#' if a[x, y] else space, end='')
        print()

def fold(a, axis='x', at_coord=0):
    """
    >>> f = StringIO(\
    '6,10\\n' \
    '0,14\\n' \
    '9,10\\n' \
    '0,3\\n' \
    '10,4\\n' \
    '4,11\\n' \
    '6,0\\n' \
    '6,12\\n' \
    '4,1\\n' \
    '0,13\\n' \
    '10,12\\n' \
    '3,4\\n' \
    '3,0\\n' \
    '8,4\\n' \
    '1,10\\n' \
    '2,14\\n' \
    '8,10\\n' \
    '9,0\\n' \
    '\\n' \
    'fold along y=7\\n' \
    'fold along x=5')
    >>> a, instructions = load(f)
    >>> a = fold(a, **instructions[0])
    >>> print_dots(a, '.')
    #.##..#..#.
    #...#......
    ......#...#
    #...#......
    .#.#..#.###
    ...........
    ...........
    >>> a = fold(a, **instructions[1])
    >>> print_dots(a, '.')
    #####
    #...#
    #...#
    #...#
    #####
    .....
    .....
    """
    arr_1, _, arr_2 = np.split(a, [at_coord, at_coord+1], axis=0 if axis == 'x' else 1)
    return np.logical_or(arr_1, np.rot90(arr_2, -1 if axis == 'x' else 1).T)

def follow_all_instructions(a, instructions):
    for i in instructions:
        a = fold(a, **i)
    return a


if __name__ == '__main__':
    with open('./input/day_13.txt', 'r') as f:
        array, folding = load(f)
    print(f'part 1: {np.sum(fold(array, **folding[0]))}')

    array = follow_all_instructions(array, folding)
    print('part 2:')
    print_dots(array)
