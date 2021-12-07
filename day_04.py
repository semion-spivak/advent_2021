import numpy as np
from io import StringIO
from itertools import product
from copy import deepcopy


class Card:
    def __init__(self, card_fh):
        self.card = np.loadtxt(card_fh, dtype=int)
        self.matches = np.zeros(self.card.shape, dtype=bool)
        self.numbers = {}
        for y, x in product(range(self.card.shape[0]), repeat=2):
            self.numbers[self.card[y, x]] = (y, x)

    def mark(self, number):
        if number in self.numbers.keys():
            y, x = self.numbers[number]
            self.matches[y, x] = True

    def has_won(self):
        for i in range(self.card.shape[0]):
            if np.all(self.matches[i, :]) or np.all(self.matches[:, i]):
                return True
        return False

    def score(self, n):
        return np.sum(np.ma.array(self.card, mask=self.matches)) * n


def load(fname):
    with open(fname, 'r') as f:
        numbers = list(map(int, next(f).strip('\n').split(',')))
        cards = set()
        while raw_card := f.read(76):
            cards.add(Card(StringIO(raw_card)))
    return numbers, cards

if __name__ == '__main__':
    numbers, cards = load('./input/day_04.txt')
    for n, c in product(numbers, deepcopy(cards)):
        c.mark(n)
        if c.has_won():
            break
    print(f'part 1: {c.score(n)}')

    for n in numbers:
        to_remove = set()
        for c in cards:
            c.mark(n)
            if c.has_won():
                to_remove.add(c)
        cards -= to_remove
        if len(cards) == 0:
            break
    print(f'part 2: {c.score(n)}')