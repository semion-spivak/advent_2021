from io import StringIO
import networkx as nx
from copy import copy
from collections import defaultdict
from pprint import pprint


def load(f):
    g = nx.Graph()
    for line in f:
        src, dst = line.strip('\n').split('-', maxsplit=1)
        g.add_edge(src, dst)
    return g

def count_paths(g, src='start', seen_lowers=None, allowed_lower=None):
    """
    >>> f = StringIO(\
    'start-A\\n' \
    'start-b\\n' \
    'A-c\\n' \
    'A-b\\n' \
    'b-d\\n' \
    'A-end\\n' \
    'b-end')
    >>> pp = count_paths(load(f))
    >>> len(pp)
    10

    >>> f = StringIO(\
    'dc-end\\n' \
    'HN-start\\n' \
    'start-kj\\n' \
    'dc-start\\n' \
    'dc-HN\\n' \
    'LN-dc\\n' \
    'HN-end\\n' \
    'kj-sa\\n' \
    'kj-HN\\n' \
    'kj-dc')
    >>> pp = count_paths(load(f))
    >>> len(pp)
    19
    """
    current_path = [src]
    if src == 'end':
        return [current_path]
    paths = []
    if seen_lowers is None:
        seen_lowers = defaultdict(int)
        seen_lowers['start'] += 1
        if allowed_lower:
            seen_lowers[allowed_lower] = -1
    elif src.islower():
        seen_lowers[src] += 1
    for adj_node in sorted(g.adj[src].keys()):
        if seen_lowers[adj_node] > 0:
            continue
        for path in count_paths(g, src=adj_node, seen_lowers=copy(seen_lowers), allowed_lower=allowed_lower):
            current_path_copy = copy(current_path)
            current_path_copy.extend(path)
            paths.append(current_path_copy)
    return paths

def part2(g):
    """
    >>> f = StringIO(\
    'start-A\\n' \
    'start-b\\n' \
    'A-c\\n' \
    'A-b\\n' \
    'b-d\\n' \
    'A-end\\n' \
    'b-end')
    >>> len(part2(load(f)))
    36
    """
    paths = set()
    for l in set(filter(lambda x: x.islower(), g.nodes)) - {'start', 'end'}:
        for p in count_paths(g, allowed_lower=l):
            paths.add(tuple(p))
    return paths

if __name__ == '__main__':
    with open('./input/day_12.txt', 'r') as f:
        g = load(f)
    print(f'part 1: {len(count_paths(g))}')
    print(f'part 2: {len(part2(g))}')
