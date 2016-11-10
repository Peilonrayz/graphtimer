from timeit import timeit
from itertools import repeat
from collections import Iterable
from textwrap import dedent

CATEGORY10 = '#1f77b4 #ff7f0e #2ca02c #d62728 #9467bd #8c564b #e377c2 #7f7f7f #bcbd22 #17becf'.split()
CATEGORY20 = '#1f77b4 #aec7e8 #ff7f0e #ffbb78 #2ca02c #98df8a #d62728 #ff9896 #9467bd #c5b0d5 #8c564b #c49c94 #e377c2 #f7b6d2 #7f7f7f #c7c7c7 #bcbd22 #dbdb8d #17becf #9edae5'.split()
CATEGORY20b = '#393b79 #5254a3 #6b6ecf #9c9ede #637939 #8ca252 #b5cf6b #cedb9c #8c6d31 #bd9e39 #e7ba52 #e7cb94 #843c39 #ad494a #d6616b #e7969c #7b4173 #a55194 #ce6dbd #de9ed6'.split()
CATEGORY20c = '#3182bd #6baed6 #9ecae1 #c6dbef #e6550d #fd8d3c #fdae6b #fdd0a2 #31a354 #74c476 #a1d99b #c7e9c0 #756bb1 #9e9ac8 #bcbddc #dadaeb #636363 #969696 #bdbdbd #d9d9d9'.split()


def _dict_function(list_):
    _function = dedent('''
    def fn({0}):
        return {{k: v for k, v in zip({1}, [{2}]) if v is not None}}
    ''')
    d = {}
    exec(_function.format(', '.join(i+'=None' for i in list_), list_, ', '.join(list_)), globals(), d)
    return d['fn']


def time(*args, **kwargs):
    local = _time_dict(*args, **kwargs)
    def wrapper(*args, **kwargs):
        global_ = _time_dict(*args, **kwargs)
        global_.update(local)
        stmt = global_.pop('stmt', 'fn(a)')
        setup = global_.pop('setup', 'a = {}')
        def inner(function, domain_value):
            return timeit(
                stmt,
                setup="from __main__ import {} as fn; {}".format(function, setup.format(domain_value)),
                **global_)
        return inner
    return wrapper


def flat(i):
    if hasattr(i, 'flat'):
        return i.flat
    if not isinstance(i, Iterable) or isinstance(i, str):
        return [i]
    l = i
    while True:
        if any(not isinstance(item, Iterable) or isinstance(item, str) for item in l):
            return l
        l = [item for iterable in l for item in iterable]


_time_dict = _dict_function(['setup', 'number', 'timer', 'globals', 'stmt'])


class GraphTimer:
    functions = []
    inputs = []
    domain = []
    titles = []
    colors = CATEGORY10

    def __init__(self, amount=1, *args, **kwargs):
        self.amount = amount
        self.timers = [
            (setup if callable(setup) else time(*flat(setup)))(*args, **kwargs)
            for setup in self.inputs
        ]
        self.domain_values = list(self.domain)

    def time_input(self, timer):
        return [
            [
                self.average_measure(timer, function, value)
                for value in self.domain_values
            ]
            for function in self.functions
        ]

    def average_measure(self, timer, function, value):
        amount = self.amount
        results = sorted(timer(function, value) for _ in range(amount))
        lower = amount // 4
        upper = amount - lower - 1
        q1 = results[lower]
        q3 = results[upper]
        conforming = [i for i in results if q1 <= i <= q3]
        mean = sum(conforming) / len(conforming)
        return mean, q1, q3

    def _graph_times(self, axis, data, area_error=True, use_errorbar=False):
        for results, color in zip(data, self.colors):
            average, lower, upper = zip(*results)
            if area_error:
                axis.fill_between(self.domain_values, lower, upper, facecolor=color, color="none", alpha=0.1)
            if use_errorbar:
                average, lower, upper = zip(*self.error_line(results))
                yield axis.errorbar(self.domain_values, average, [lower, upper], color=color)
            else:
                yield axis.plot(self.domain_values, average, color=color)[0]

    def graph_times(self, axis, data, area_error=True, legend=True, title=None, use_errorbar=False):
        lines = list(self._graph_times(axis, data, area_error, use_errorbar))
        if title is not None and hasattr(axis, 'set_title'):
            axis.set_title(title)
        if legend and hasattr(axis, 'legend'):
            axis.legend(lines, self.functions, loc=0)
        return lines

    @staticmethod
    def error_line(results):
        for average, minimum, maximum in results:
            yield average, average - minimum, maximum - average

    def plot_axis(self, axis, timer, area_error=True, legend=True, title=None, use_errorbar=False):
        times = self.time_input(timer)
        return list(self.graph_times(axis, times, area_error, legend, title, use_errorbar))

    def plot_axes(self, axes, area_error=True, legend=True, show_titles=False, use_errorbar=False):
        titles = self.titles if show_titles else repeat(None)
        return [
            self.plot_axis(axis, timer, area_error, legend, title, use_errorbar)
            for axis, timer, title in zip(axes, self.timers, titles)
        ]
