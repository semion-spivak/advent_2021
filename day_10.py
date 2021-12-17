from collections import deque
from functools import lru_cache


opening = {'{': '}', '(': ')', '[': ']', '<': '>'}
error_cost = {')': 3, ']': 57, '}': 1197, '>': 25137}
completion_cost = {')': 1, ']': 2, '}': 3, '>': 4}

def load(f):
    data = []
    for line in f:
        data.append(line.strip('\n'))
    return data

@lru_cache
def find_error(line):
    """
    >>> find_error('{([(<{}[<>[]}>{[]{[(<()>')
    '}'
    >>> find_error('[[<[([]))<([[{}[[()]]]')
    ')'
    >>> find_error('[{[{({}]{}}([{[{{{}}([]')
    ']'
    >>> find_error('[<(<(<(<{}))><([]([]()')
    ')'
    >>> find_error('<{([([[(<>()){}]>(<<{{')
    '>'
    >>> find_error('[({(<(())[]>[[{[]{<()<>>')
    deque([']', ')', '}', ')', ']', ']', '}', '}'])
    """
    l = deque(line)
    mirror = deque()
    while l:
        p = l.popleft()
        if p in opening.keys():
            mirror.append(opening[p])
        else:
            q = mirror.pop()
            if q != p:
                return p
    return mirror

def filter_errors(data, etype):
    return filter(lambda x: isinstance(x, etype), map(find_error, data))

def total_error_score(data):
    return sum(map(error_cost.get, filter_errors(data, str)))

def autocomplete_score(data):
    """
    >>> data = ['[({(<(())[]>[[{[]{<()<>>', \
                '[(()[<>])]({[<{<<[]>>(', \
                '{([(<{}[<>[]}>{[]{[(<()>', \
                '(((({<>}<{<{<>}{[]{[]{}', \
                '[[<[([]))<([[{}[[()]]]', \
                '[{[{({}]{}}([{[{{{}}([]', \
                '{<[[]]>}<{[{[{[]{()[[[]', \
                '[<(<(<(<{}))><([]([]()', \
                '<{([([[(<>()){}]>(<<{{', \
                '<{([{{}}[<[[[<>{}]]]>[]]']
    >>> autocomplete_score(data)
    288957
    """
    totals = []
    for e in filter_errors(data, deque):
        total = 0
        while e:
            total = total * 5 + completion_cost[e.pop()]
        totals.append(total)
    return sorted(totals)[(len(totals) // 2)]

if __name__ == '__main__':
    with open('./input/day_10.txt', 'r') as f:
        data = load(f)
    print(f'part 1: {total_error_score(data)}')
    print(f'part 2: {autocomplete_score(data)}')
