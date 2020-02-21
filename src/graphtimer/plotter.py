import numpy as np

from . import helpers
from .graph import MatPlotLib


class Plotter:
    """Interface to the timer object. Returns objects made to ease usage."""

    def __init__(self, timer):
        self.timer = getattr(timer, "multi_timer", timer)

    def timeit(self, number, domain, *args, **kwargs):
        """Interface to self.timer.timeit. Returns a PlotValues."""
        return self.repeat(1, number, domain, *args, **kwargs).min(errors=None)

    def repeat(self, repeat, number, domain, *args, **kwargs):
        """Interface to self.timer.repeat. Returns a PlotTimings."""
        return PlotTimings(
            self.timer.repeat(domain, repeat, number, *args, **kwargs),
            {"functions": self.timer.functions, "domain": domain},
        )


class PlotTimings:
    """Thin interface over _DataSet"""

    def __init__(self, data, kwargs):
        self.data = data
        self.kwargs = kwargs

    def quartile(self, quartile, *, errors=None, outlier=1.5, axis=2):
        """Interface to _DataSet.quartile and errors. Returns a PlotValues."""
        return PlotValues(
            np.apply_along_axis(helpers.quartile, axis, self.data, outlier, quartile,),
            np.apply_along_axis(
                helpers.errors, axis, self.data, outlier, np.array(errors),
            ),
            self.kwargs,
        )

    def min(self, *, errors=((-1, 3),), outlier=1.5):
        """Return the Q1 value and show the error from Q-1 Q3."""
        return self.quartile(0, errors=errors, outlier=outlier)

    def max(self, *, errors=((1, 5),), outlier=1.5):
        """Return the Q4 value and show the error from Q1 Q5."""
        return self.quartile(4, errors=errors, outlier=outlier)

    def mean(self, start=0, end=4, *, errors=((1, 3),), outlier=1.5, axis=2):
        """Interface to _DataSet.mean and errors. Returns a PlotValues."""
        return PlotValues(
            np.apply_along_axis(helpers.mean, axis, self.data, outlier, start, end,),
            np.apply_along_axis(
                helpers.errors, axis, self.data, outlier, np.array(errors),
            ),
            self.kwargs,
        )


class PlotValues:
    """Thin interface to Graph.graph."""

    def __init__(self, values, errors, kwargs):
        self.values = values
        self.errors = errors
        self.kwargs = kwargs

    def plot(self, graph, graph_lib=MatPlotLib, **kwargs):
        g = graph_lib()
        return g.graph(
            graph,
            self.values,
            self.errors,
            self.kwargs.pop("domain"),
            functions=self.kwargs.pop("functions"),
            **kwargs
        )
