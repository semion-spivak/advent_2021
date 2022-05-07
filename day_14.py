from collections import Counter, defaultdict as dd
from io import StringIO
from itertools import tee
from copy import copy
import re

insert_pattern = re.compile(r'^([A-Z]{2}) -> ([A-Z])$', re.MULTILINE)

def load(f):
    rules = dict()
    initial = f.readline().rstrip()
    f.readline()
    for k, v in insert_pattern.findall(f.read()):
        rules[tuple(k)] = v
    return initial, rules

def pairwise(data):
    a, b = tee(data)
    next(b, None)
    return zip(a, b)

def polymerize(template, rules, steps=1):
    """
    >>> f = StringIO(\
    'NNCB\\n' \
    '\\n' \
    'CH -> B\\n' \
    'HH -> N\\n' \
    'CB -> H\\n' \
    'NH -> C\\n' \
    'HB -> C\\n' \
    'HC -> B\\n' \
    'HN -> C\\n' \
    'NN -> C\\n' \
    'BH -> H\\n' \
    'NC -> B\\n' \
    'NB -> B\\n' \
    'BN -> B\\n' \
    'BB -> N\\n' \
    'BC -> B\\n' \
    'CC -> N\\n' \
    'CN -> C')
    >>> initial, rules = load(f)
    >>> polymerize(initial, rules)
    'NCNBCHB'

    >>> polymerize(initial, rules, 2)
    'NBCCNBBBCBHCB'

    >>> polymerize(initial, rules, 3)
    'NBBBCNCCNBBNBNBBCHBHHBCHB'

    >>> polymerize(initial, rules, 4)
    'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    """
    for _ in range(steps):
        to_insert = []
        for pos, pair in enumerate(pairwise(template)):
            to_insert.append((pos, rules[pair]))

        offset = 1
        for pos, letter in to_insert:
            template = template[:pos + offset] + letter + template[pos + offset:]
            offset += 1
    return template

def part_1(initial, rules, steps=10):
    result = polymerize(initial, rules, steps)
    cnt = Counter(result)
    return max(cnt.values()) - min(cnt.values())


def part_2(template, rules, steps):
    """
    >>> f = StringIO(\
    'NNCB\\n' \
    '\\n' \
    'CH -> B\\n' \
    'HH -> N\\n' \
    'CB -> H\\n' \
    'NH -> C\\n' \
    'HB -> C\\n' \
    'HC -> B\\n' \
    'HN -> C\\n' \
    'NN -> C\\n' \
    'BH -> H\\n' \
    'NC -> B\\n' \
    'NB -> B\\n' \
    'BN -> B\\n' \
    'BB -> N\\n' \
    'BC -> B\\n' \
    'CC -> N\\n' \
    'CN -> C')
    >>> initial, rules = load(f)
    >>> part_2(initial, rules, 10)
    1588
    """
    pairs_count = dd(int)
    cnt = dd(int)
    initial_count = Counter(template)
    cnt.update(initial_count)
    for pair in pairwise(template):
        pairs_count[pair] += 1

    for _ in range(steps):
        pos_copy = copy(pairs_count)
        to_decrease = dd(int)
        for pair, letter in rules.items():
            a, b = pair
            orig = pairs_count[pair]
            if orig > 0:
                pos_copy[(a, letter)] += orig
                pos_copy[(letter, b)] += orig
                cnt[letter] += orig
                to_decrease[pair] += orig
        pairs_count = pos_copy
        for pair, value in to_decrease.items():
            pairs_count[pair] -= value
    return max(cnt.values()) - min(cnt.values())


if __name__ == '__main__':
    with open('input/day_14.txt', 'r') as f:
        initial, rules = load(f)
    print(f'Day 14, part 1: {part_1(copy(initial), rules, 10)}')
    print(f'Day 14, part 2: {part_2(initial, rules, 40)}')
