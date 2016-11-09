from timeit import timeit
from itertools import repeat

CATEGORY10 = '#1f77b4 #ff7f0e #2ca02c #d62728 #9467bd #8c564b #e377c2 #7f7f7f #bcbd22 #17becf'.split()
CATEGORY20 = '#1f77b4 #aec7e8 #ff7f0e #ffbb78 #2ca02c #98df8a #d62728 #ff9896 #9467bd #c5b0d5 #8c564b #c49c94 #e377c2 #f7b6d2 #7f7f7f #c7c7c7 #bcbd22 #dbdb8d #17becf #9edae5'.split()
CATEGORY20b = '#393b79 #5254a3 #6b6ecf #9c9ede #637939 #8ca252 #b5cf6b #cedb9c #8c6d31 #bd9e39 #e7ba52 #e7cb94 #843c39 #ad494a #d6616b #e7969c #7b4173 #a55194 #ce6dbd #de9ed6'.split()
CATEGORY20c = '#3182bd #6baed6 #9ecae1 #c6dbef #e6550d #fd8d3c #fdae6b #fdd0a2 #31a354 #74c476 #a1d99b #c7e9c0 #756bb1 #9e9ac8 #bcbddc #dadaeb #636363 #969696 #bdbdbd #d9d9d9'.split()


def time(setup, param='a'):
    def wrapper(function, domain_value, number):
        user_setup = setup.format(domain_value)
        return timeit(
            '{}({})'.format(function, param),
            setup="from __main__ import {}; {}".format(function, user_setup),
            number=number)
    return wrapper


def flat(axes):
    if hasattr(axes, 'flat'):
        return axes.flat
    try:
        return [axis for row in axes for axis in row]
    except TypeError:
        return [axes]


class GraphTimer:
    functions = []
    inputs = []
    domain = []
    titles = []
    colors = CATEGORY10

    def __init__(self, amount, number):
        self.amount = amount
        self.number = number
        self.setups = [
            time(setup) if isinstance(setup, str) else setup
            for setup in self.inputs]
        self.domain_values = list(self.domain)

    def time_input(self, input):
        return [
            [
                self.average_measure(input, function, value)
                for value in self.domain_values
            ] for function in self.functions
        ]

    def average_measure(self, input, function, value):
        results = sorted(input(function, value, self.number)
                         for _ in range(self.amount))
        lower = self.amount // 4
        upper = self.amount - lower - 1
        q1 = results[lower]
        q3 = results[upper]
        conforming = [i for i in results if q1 <= i <= q3]
        mean = sum(conforming) / len(conforming)
        return mean, q1, q3

    def graph_times(self, axis, data, box_error=True, use_errorbar=False):
        for results, color in zip(data, self.colors):
            stats = self.error_line(results) if use_errorbar else results
            average, lower, upper = zip(*stats)
            if box_error:
                if use_errorbar:
                    yield axis.errorbar(
                            self.domain_values, average,
                            yerr=(lower, upper), color=color)[0]
                    continue
                else:
                    axis.fill_between(
                            self.domain_values, lower, upper,
                            facecolor=color, color="none", alpha=0.1)
            yield axis.plot(self.domain_values, average, color=color)[0]

    @staticmethod
    def error_line(results):
        for average, minimum, maximum in results:
            yield average, average - minimum, maximum - average

    def plot_axis(self, axis, setup, box_error=True, legend=True, title=None, use_errorbar=False):
        times = self.time_input(setup)
        graph = list(self.graph_times(axis, times, box_error, use_errorbar))

        if title is not None and hasattr(axis, 'set_title'):
            axis.set_title(title)
        if legend and hasattr(axis, 'legend'):
            axis.legend(graph, self.functions, loc=0)

        return graph

    def plot_axes(self, axes, box_error=True, legend=True, show_titles=False, use_errorbar=False):
        titles = self.titles if show_titles else repeat(None)
        return [
            self.plot_axis(axis, setup, box_error, legend, title, use_errorbar)
            for axis, setup, title in zip(axes, self.setups, titles)
        ]
