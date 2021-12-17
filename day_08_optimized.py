from collections import Counter
from io import StringIO
from itertools import chain, starmap, tee
from copy import copy

digit_to_segments_count = {1: 2, 4: 4, 7: 3, 8: 7}
segments_count_to_digit = {2: 1, 4: 4, 3: 7, 7: 8}

def load(h):
    out = []
    for line in h:
        patterns, value = line.strip('\n').split(' | ')
        out.append((tuple(map(frozenset, patterns.split(' '))), tuple(map(frozenset, value.split(' ')))))
    return out

def count_simple_digits(data):
    """
    >>> h = StringIO(\
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\\n' \
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\\n' \
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\\n' \
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\\n' \
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\\n' \
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\\n' \
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\\n' \
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\\n' \
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\\n' \
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce')
    >>> count_simple_digits(load(h))
    26
    """
    c = Counter(chain(*[[len(j) for j in i] for _, i in data]))
    return sum([c[digit_to_segments_count[i]] for i in (1, 4, 7, 8)])

def decode_line(digits, number):
    """
    >>> h = StringIO('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf')
    >>> decode_line(*(load(h)[0]))
    5353
    """
    sig2int = dict()
    int2sig = dict()
    unsolved = set(digits)

    def register(d, value):
        int2sig[value] = d
        sig2int[d] = value
        unsolved.remove(d)

    # register 1, 4, 7, 8 by known unique lengths
    for d, d_len in zip(digits, map(len, digits)):
        if d_len in segments_count_to_digit.keys():
            register(d, segments_count_to_digit[d_len])

    # https://github.com/mattvperry/aoc2021/blob/main/day8/day8.ts
    left_bottom = int2sig[8] - int2sig[7] - int2sig[4]
    left_middle = int2sig[4] - int2sig[1]

    u1, u2 = tee(copy(unsolved), 2)
    for d, len_d in zip(u1, map(len, u2)):
        if len_d == 5:
            if d.issuperset(int2sig[7]):
                register(d, 3)
            elif d.issuperset(left_middle):
                register(d, 5)
            elif d.issuperset(left_bottom):
                register(d, 2)
        elif len_d == 6:
            if not d.issuperset(int2sig[7]):
                register(d, 6)
            elif not d.issuperset(left_bottom):
                register(d, 9)
            elif not d.issuperset(left_middle):
                register(d, 0)
    out = 0
    for n in number:
        out = out * 10 + sig2int[n]
    return out

if __name__ == '__main__':
    with open('./input/day_08.txt', 'r') as f:
        data = load(f)
    print(f'part 1: {count_simple_digits(data)}')
    print(f'part 2: {sum(starmap(decode_line, data))}')
