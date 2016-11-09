import matplotlib.pyplot as plt
from graphtimer import flat, GraphTimer


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


class Timer(GraphTimer):
    functions = [
        'list_comp',
        'list_append',
    ]
    inputs = [
        'a = range({})',
        'a = list(range({}))',
        'from __main__ import UnoptimisedRange as range; a = range({})',
    ]
    domain = range(0, 10001, 1000)
    titles = [
        'Range',
        'List',
        'Unoptimised',
    ]

def main():
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
    Timer(amount=10, number=100).plot_axes(flat(axs), show_titles=True, use_errorbar=True)
    plt.show()

if __name__ == '__main__':
    main()
