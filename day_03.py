from collections import Counter
import numpy as np

with open('./input/day_03.txt', 'r') as f:
    data = np.array([list(map(int, list(line.strip('\n')))) for line in f])

def power_consumption():
    most, least = 0, 0
    for x in range(data.shape[1]):
        c = Counter(data[:, x])
        most = (most << 1) + max(c, key=c.get)
        least = (least << 1) + min(c, key=c.get)
    return most * least

def component_rating(tie_break=1, compare=max):
    rating = 0
    _data = data.copy()
    for x in range(data.shape[1]):
        c = Counter(_data[:, x])
        bit = tie_break if c[0] == c[1] else compare(c, key=c.get)
        rating = (rating << 1) + bit
        _data = _data[_data[:, x] == bit]
    return rating

def life_support_rating():
    oxy_args, co2_args = (1, max), (0, min)
    return component_rating(*oxy_args) * component_rating(*co2_args)

if __name__ == '__main__':
    print(f'part 1: {power_consumption()}')
    print(f'part 1: {life_support_rating()}')
