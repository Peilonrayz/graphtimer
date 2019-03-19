from .graph import MatPlotLib


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


class _DataSet:
    """Holds timeit values and defines statistical methods around them."""
    def __init__(self, values):
        self.values = sorted(values)

    def quartile_indexes(self, outlier):
        """Generates the quartile indexes. Uses tukey's fences to remove outliers."""
        delta = (len(self.values) - 1) / 4
        quartiles = [int(round(delta * i)) for i in range(5)]
        if outlier is not None:
            if outlier < 0:
                raise ValueError("outlier should be non-negative.")
            iqr = outlier * (self.values[quartiles[3]] - self.values[quartiles[1]])
            low = self.values[quartiles[1]] - iqr
            high = self.values[quartiles[3]] + iqr

            for i, v in enumerate(self.values):
                if v >= low:
                    quartiles[0] = i
                    break

            for i, v in reversed(list(enumerate(self.values))):
                if v <= high:
                    quartiles[4] = i
                    break
        return tuple(quartiles)

    def errors(self, errors, outlier):
        """Returns tuples containing the quartiles wanted."""
        if errors is None:
            return None
        quartiles = self.quartile_indexes(outlier)
        # Allow out of quartile error bars using -1 and 5.
        quartiles += (-1, 0)
        return [
            (
                self.values[quartiles[start]],
                self.values[quartiles[stop]]
            )
            for start, stop in errors
        ]

    def quartile(self, quartile, outlier):
        """Return the value of the quartile provided."""
        quartiles = self.quartile_indexes(outlier)
        return self.values[quartiles[quartile]]

    def mean(self, start, end, outlier):
        """Return the mean of the values over the quartiles specified."""
        quartiles = self.quartile_indexes(outlier)
        start = quartiles[start]
        end = quartiles[end]
        return sum(self.values[start:end + 1]) / (1 + end - start)


class PlotTimings:
    """Thin interface over _DataSet"""
    def __init__(self, data, kwargs):
        self.data = [
            [_DataSet(results) for results in function_values]
            for function_values in data
        ]
        self.kwargs = kwargs

    def quartile(self, quartile, *, errors=None, outlier=1.5):
        """Interface to _DataSet.quartile and errors. Returns a PlotValues."""
        return PlotValues(
            [
                [
                    _DataValues(
                        ds.quartile(quartile, outlier),
                        ds.errors(errors, outlier)
                    )
                    for ds in function_values
                ]
                for function_values in self.data
            ],
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
                    _DataValues(
                        ds.mean(start, end, outlier),
                        ds.errors(errors, outlier)
                    )
                    for ds in function_values
                ]
                for function_values in self.data
            ],
            self.kwargs
        )


class _DataValues:
    """Holds the wanted statistical data from the timings."""
    def __init__(self, value, errors):
        self.value = value
        self.errors = errors


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
