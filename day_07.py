from io import StringIO
from collections import Counter

def load(h):
    return list(map(int, h.read().strip('\n').split(',')))

def progression(n):
    """
    >>> progression(0)
    0
    >>> progression(1)
    1
    >>> progression(2)
    3
    >>> progression(3)
    6
    """
    return sum(range(1, n+1))

def alignment_cost(positions, cost_func=lambda x: x):
    """
    >>> h = StringIO('16,1,2,0,4,2,7,1,2,14')
    >>> alignment_cost(load(h))
    37

    >>> h = StringIO('16,1,2,0,4,2,7,1,2,14')
    >>> alignment_cost(load(h), progression)
    168
    """
    c = Counter(positions)
    min_cost = 2 ** 32 - 1
    for pos in range(min(c.keys()), max(c.keys())+1):
        cost = 0
        for sub_pos, cnt in c.items():
            cost += cost_func(abs(pos-sub_pos)) * cnt
        min_cost = min(min_cost, cost)
    return min_cost

if __name__ == '__main__':
    with open('./input/day_07.txt', 'r') as f:
        positions = load(f)
    print(f'part 1: {alignment_cost(positions)}')
    print(f'part 2: {alignment_cost(positions, progression)}')