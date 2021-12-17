import networkx as nx
import numpy as np
from itertools import starmap

adj = ((-1, 0), (0, -1), (1, 0), (0, 1))
plus_one_idx = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 1}
plus_one = np.vectorize(plus_one_idx.get)

max_x, max_y = 0, 0
data, G = None, None


def load(f, expand=False):
    global max_x, max_y, data, G
    f.seek(0)
    max_x, max_y = 0, 0
    rows = []
    for y, line in enumerate(f):
        row = []
        for x, level in enumerate(map(int, line.strip('\n'))):
            row.append(level)
        rows.append(np.hstack(row))
    data = np.vstack(rows)

    if expand:
        rows = []
        row = [data]
        for _x in range(4):
            row.append(plus_one(row[-1]))
        rows.append(np.hstack(row))

        for _y in range(4):
            rows.append(plus_one(rows[-1]))
        data = np.vstack(rows)

    max_x, max_y = tuple(map(lambda x: x-1, data.shape))

    G = nx.DiGraph()
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            for dx, dy in adj:
                _x, _y = x+dx, y+dy
                if _x < 0 or _x > max_x or _y < 0 or _y > max_y:
                    continue
                G.add_edge((y, x), (_y, _x), weight=data[_y, _x])

def lowest_total_risk(f, expand=False):
    """
    >>> with open('./input./day_15_test.txt', 'r') as f:
    ...     lowest_total_risk(f)
    40

    >>> with open('./input./day_15_test.txt', 'r') as f:
    ...     lowest_total_risk(f, expand=True)
    315
    """
    load(f, expand=expand)
    p = nx.dijkstra_path(G, (0, 0), (max_x, max_y))
    return sum(starmap(lambda y, x: data[y, x], p[1:]))


if __name__ == '__main__':
    with open('./input/day_15.txt', 'r') as f:
        print(f'part 1: {lowest_total_risk(f)}')
        print(f'part 2: {lowest_total_risk(f, expand=True)}')
