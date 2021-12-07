from collections import defaultdict as dd
import re

pat = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)$')

with open('./input/day_05.txt', 'r') as f:
    data = [tuple(map(int, pat.match(line).groups())) for line in f]

def natural_range(a, b):
    step = 1 if b >= a else -1
    return range(a, b + step, step)

def overlaps(count_diagonal=False):
    diagram = dd(int)
    for src_x, src_y, dst_x, dst_y in data:
        if src_x == dst_x:
            for y in natural_range(src_y, dst_y):
                diagram[(src_x, y)] += 1
        elif src_y == dst_y:
            for x in natural_range(src_x, dst_x):
                diagram[(x, src_y)] += 1
        elif count_diagonal:
            for x, y in zip(natural_range(src_x, dst_x),
                            natural_range(src_y, dst_y)):
                diagram[(x, y)] += 1
    return len([v for v in diagram.values() if v > 1])

if __name__ == '__main__':
    print(f'part 1: {overlaps()}')
    print(f'part 2: {overlaps(count_diagonal=True)}')
