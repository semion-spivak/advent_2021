from io import StringIO
import networkx as nx
from functools import reduce
from operator import mul

G = nx.DiGraph()
adj = ((-1, 0), (0, 1), (1, 0), (0, -1))

def load(f):
    G.clear()
    max_y, max_x = 0, 0
    for y, line in enumerate(f):
        for x, height in enumerate(map(int, list(line.strip('\n')))):
            G.add_node((y, x), height=height)
            max_x = max(max_x, x)
        max_y = max(max_y, y)

    # populate edges
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            h = G.nodes(data=True)[(y, x)]['height']
            for dy, dx in adj:
                adj_y, adj_x = y + dy, x + dx
                if adj_y < 0 or adj_y > max_y or adj_x < 0 or adj_x > max_x:
                    continue
                adj_h = G.nodes(data=True)[(adj_y, adj_x)]['height']
                if h >= adj_h:
                    G.add_edge((y, x), (adj_y, adj_x))

def lowest_nodes():
    return (node for node in G.nodes if G.out_degree(node) == 0)

def risk_levels_sum():
    """
    >>> f = StringIO(\
    '2199943210\\n' \
    '3987894921\\n' \
    '9856789892\\n' \
    '8767896789\\n' \
    '9899965678')
    >>> load(f)
    >>> risk_levels_sum()
    15
    """
    return sum(map(lambda node: G.nodes(data=True)[node]['height']+1, lowest_nodes()))

def three_largest_basins():
    """
    >>> f = StringIO(\
    '2199943210\\n' \
    '3987894921\\n' \
    '9856789892\\n' \
    '8767896789\\n' \
    '9899965678')
    >>> load(f)
    >>> three_largest_basins()
    1134
    """
    hide_nine = lambda n: G.nodes(data=True)[n]['height'] != 9
    subgraph = nx.subgraph_view(G.reverse(), filter_node=hide_nine)
    basins = [len(nx.bfs_tree(subgraph, n)) for n in lowest_nodes()]
    return reduce(mul, sorted(basins, reverse=True)[:3])


if __name__ == '__main__':
    with open('./input/day_09.txt', 'r') as f:
        load(f)
    print(f'part 1: {risk_levels_sum()}')
    print(f'part 2: {three_largest_basins()}')
