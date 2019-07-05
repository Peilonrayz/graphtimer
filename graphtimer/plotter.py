import numpy as np
import functools

from .graph import MatPlotLib
from . import helpers


class Plotter:
    """Interface to the timer object. Returns objects made to ease usage."""
    def __init__(self, timer):
        self.timer = getattr(timer, 'multi_timer', timer)

    def timeit(self, number, domain, *args, **kwargs):
        """Interface to self.timer.timeit. Returns a PlotValues."""
        return self.repeat(1, number, domain, *args, **kwargs).min(errors=None)

    def repeat(self, repeat, number, domain, *args, **kwargs):
        """Interface to self.timer.repeat. Returns a PlotTimings."""
        return PlotTimings(
            self.timer.repeat(domain, repeat, number, *args, **kwargs),
            {
                'functions': self.timer.functions,
                'domain': domain
            }
        )


class PlotTimings:
    """Thin interface over _DataSet"""
    def __init__(self, data, kwargs):
        self.data = [
            [results for results in function_values]
            for function_values in data
        ]
        self.kwargs = kwargs

    def quartile(self, quartile, *, errors=None, outlier=1.5):
        """Interface to _DataSet.quartile and errors. Returns a PlotValues."""
        return PlotValues(
            helpers.quartiles(self.data, outlier, quartile, errors, 2),
            self.kwargs
        )

    def min(self, *, errors=((-1, 3),), outlier=1.5):
        """Return the Q1 value and show the error from Q-1 Q3."""
        return self.quartile(0, errors=errors, outlier=outlier)

    def max(self, *, errors=((1, 5),), outlier=1.5):
        """Return the Q4 value and show the error from Q1 Q5."""
        return self.quartile(4, errors=errors, outlier=outlier)

    def mean(self, start=0, end=4, *, errors=((1, 3),), outlier=1.5):
        """Interface to _DataSet.mean and errors. Returns a PlotValues."""
        return PlotValues(
            [
                [
                    helpers.mean(values, outlier, start, end, errors)
                    for values in function_values
                ]
                for function_values in self.data
            ],
            self.kwargs
        )


class PlotValues:
    """Thin interface to Graph.graph."""
    def __init__(self, data, kwargs):
        self.data = data
        self.kwargs = kwargs

    def plot(self, graph, graph_lib=MatPlotLib, **kwargs):
        g = graph_lib()
        return g.graph(
            graph,
            self.data,
            self.kwargs.pop('domain'),
            functions=self.kwargs.pop('functions'),
            **kwargs
        )
