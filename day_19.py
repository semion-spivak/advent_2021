import re
import networkx as nx
import numpy as np
from itertools import combinations, permutations, tee
from collections import defaultdict as dd


id_pat = re.compile(r'--- scanner (\d+) ---')
coords_pat = re.compile(r'(-?\d+),(-?\d+),(-?\d+)')

scanners = {}
offset_graph = nx.DiGraph()
triplets = dict()

def recalculate_triplets(scanner_id, arr):
    global triplets
    triplets[scanner_id] = dict()
    g = nx.Graph()
    for p1, p2 in combinations(arr, 2):
        d = np.sum(np.abs(p1 - p2))
        g.add_edge(tuple(p1), tuple(p2), distance=d)
    for c in g:
        a, b = sorted(g.adj[c], key=lambda x: g.edges[{x, c}]["distance"])[:2]
        a_b = g.edges[{a, b}]["distance"]
        c_a = g.edges[{a, c}]["distance"]
        c_b = g.edges[{b, c}]["distance"]
        _sum = sum((c_a ** 2, c_b ** 2, a_b ** 2))
        triplets[scanner_id][_sum] = {c_a: {c, a}, c_b: {c, b}, a_b: {a, b}}


def load(f):
    """
    >>> with open('./input/day_19_test.txt', 'r') as f:
    ...     load(f)
    >>> assert len(scanners) == 5
    >>> assert len(scanners[0]) == 25
    >>> assert len(scanners[1]) == 25
    >>> assert len(scanners[2]) == 26
    >>> assert len(scanners[3]) == 25
    >>> assert len(scanners[4]) == 26
    """
    global scanners, triplets
    beacons = dd(list)
    while line := f.readline():
        scanner_id = int(id_pat.match(line).groups()[0])
        while coords := coords_pat.match(f.readline()):
            beacons[scanner_id].append(tuple(map(int, coords.groups())))

    for scanner_id, coords_list in beacons.items():
        arr = np.array(coords_list, dtype=np.int16)
        recalculate_triplets(scanner_id, arr)
        scanners[scanner_id] = arr

shuffle_axii = (
                  lambda x: x,
                  lambda x: x[:, [0, 2, 1]],
                  lambda x: x[:, [1, 0, 2]],
                  lambda x: x[:, [1, 2, 0]],
                  lambda x: x[:, [2, 0, 1]],
                  lambda x: x[:, [2, 1, 0]],
)

flip_polarity = (
                  lambda x: x,
                  lambda x: x * [1, 1, -1],
                  lambda x: x * [1, -1, 1],
                  lambda x: x * [1, -1, -1],
                  lambda x: x * [-1, 1, 1],
                  lambda x: x * [-1, 1, -1],
                  lambda x: x * [-1, -1, 1],
                  lambda x: x * [-1, -1, -1],
)

def reorient(x):
    for ia, axis_func in enumerate(shuffle_axii):
        for ip, polar_func in enumerate(flip_polarity):
            yield ia, ip, polar_func(axis_func(x))

def realign(ar, pr, offset, x):
    ar = ar % (len(shuffle_axii))
    pr = pr % (len(flip_polarity))
    return flip_polarity[pr](shuffle_axii[ar](x)) + offset

def align(a, b):
    for ia, ip, rot_b in reorient(b):
        diff = a - rot_b
        if all([np.all(diff[0, col] == diff[:, col]) for col in (0, 1, 2)]):
            return ia, ip, diff[0, :]
    return None, None, None


def join_by_12(id_A, id_B):
    """
    >>> with open('./input/day_19_test.txt', 'r') as f:
    ...     load(f)
    >>> join_by_12(0, 1)
    (0, 5, array([   68, -1246,   -43]))
    """
    global scanners, triplets
    neighbours_a, neighbours_b = set(triplets[id_A].keys()), set(triplets[id_B].keys())
    common = neighbours_a.intersection(neighbours_b)
    if len(common) < 4:
        return None, None, None

    points_A, points_B = [], []
    for distance_sum in common:
        triple_A = triplets[id_A][distance_sum]
        triple_B = triplets[id_B][distance_sum]

        c_a, c_b, a_b = triple_A.keys()

        Aa = triple_A[c_a].intersection(triple_A[a_b]).pop()
        Ab = triple_A[c_b].intersection(triple_A[a_b]).pop()
        Ac = triple_A[c_a].intersection(triple_A[c_b]).pop()
        points_A.extend([Aa, Ab, Ac])

        Ba = triple_B[c_a].intersection(triple_B[a_b]).pop()
        Bb = triple_B[c_b].intersection(triple_B[a_b]).pop()
        Bc = triple_B[c_a].intersection(triple_B[c_b]).pop()
        points_B.extend([Ba, Bb, Bc])

    return align(np.array(points_A), np.array(points_B))

def solve_pt1():
    """
    >>> with open('./input/day_19_test.txt', 'r') as f:
    ...     load(f)
    >>> solve_pt1()
    79
    """
    global scanners, triplets, offset_graph

    offset_graph = nx.DiGraph()
    for id_A, id_B in permutations(scanners.keys(), 2):
        rot_axis, rot_polarity, offset = join_by_12(id_A, id_B)
        if offset is not None:
            offset_graph.add_edge(id_B, id_A, rot_attrs=(rot_axis, rot_polarity, offset))

    out = scanners[0].copy()
    for i in set(scanners.keys()) - {0}:
        p1, p2 = tee(nx.dijkstra_path(offset_graph, i, 0), 2)
        next(p2)
        current = scanners[i].copy()
        for a, b in zip(p1, p2):
            _rot_axis, _rot_polarity, _offset = offset_graph.edges[(a, b)]['rot_attrs']
            current = realign(_rot_axis, _rot_polarity, _offset, current)
        out = np.vstack((out, current))

    out_set = set()
    for row in out:
        out_set.add(tuple(row))

    return len(out_set)

def solve_pt2():
    """
    >>> with open('./input/day_19_test.txt', 'r') as f:
    ...     load(f)
    >>> _ = solve_pt1()
    >>> solve_pt2()
    3621
    """
    global scanners, triplets, offset_graph

    max_len = 0
    for id_A, id_B in combinations(scanners.keys(), 2):
        p1, p2 = tee(nx.dijkstra_path(offset_graph, id_A, id_B), 2)
        next(p2)
        current = np.array([[0, 0, 0]])
        for a, b in zip(p1, p2):
            _rot_axis, _rot_polarity, _offset = offset_graph.edges[(a, b)]['rot_attrs']
            current = realign(_rot_axis, _rot_polarity, _offset, current)
        max_len = max(max_len, np.sum(np.abs(current)))
    return max_len


if __name__ == '__main__':
    with open('./input/day_19.txt', 'r') as f:
        load(f)
        print(f'part 1: {solve_pt1()}')
        print(f'part 2: {solve_pt2()}')
