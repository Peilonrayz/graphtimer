from itertools import islice

class UnoptimisedRange(object):
    def __init__(self, size):
        self.size = size
    
    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError()
        return i

def list_comp(iterable):
    return [i for i in iterable]

def list_append(iterable):
    a = []
    append = a.append
    for i in iterable:
        append(i)
    return a

import matplotlib.pyplot as plt
from graphtimer import time, flat, GraphTimer

class Timer(GraphTimer):
    functions = [
        'list_comp',
        'list_append',
    ]
    inputs = [
        time('from __main__ import {} as fn; a = range({})', number=100),
        time('from __main__ import {} as fn; a = list(range({}))', number=100),
        time('from __main__ import {} as fn, UnoptimisedRange as range; a = range({})', number=100),
    ]
    domain = list(range(0, 1001, 100))
    titles = [
        'Range',
        'List',
        'Unoptimised',
    ]

def main():
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
    Timer().plot_axes(flat(axs), amount=1, show_titles=True)
    plt.show()

if __name__ == '__main__':
    main()
