import functools

import numpy as np


class _DataValues:
    """Holds the wanted statistical data from the timings."""
    def __init__(self, value, errors):
        self.value = value
        self.errors = errors


class statistics:
    @staticmethod
    def quartiles(values, outlier=1.5):
        quartiles = (
            np.linspace(0, len(values) - 1, num=5)
                .round()
                .astype('int')
                .tolist()
        )

        if outlier is not None:
            if outlier < 0:
                raise ValueError("outlier should be non-negative.")
            q75, q25 = np.percentile(values, [75, 25])
            iqr = outlier * (q75 - q25)
            low = q25 - iqr
            high = q75 + iqr
            quartiles[0] = np.argmax(values >= low)
            quartiles[4] = len(values) - np.argmax(values[::-1] <= high) - 1
        return tuple(quartiles) + (-1, 0)

    @staticmethod
    def errors(values, outlier, errors):
        """Returns tuples containing the quartiles wanted."""
        if errors is None:
            return None
        qs = statistics.quartiles(values, outlier)
        return [
            (
                values[qs[start]],
                values[qs[stop]]
            )
            for start, stop in errors
        ]

    @staticmethod
    def quartile(values, outlier, quartile):
        """Return the value of the quartile provided."""
        qs = statistics.quartiles(values, outlier)
        return values[qs[quartile]]

    @staticmethod
    def mean(values, outlier, start, end):
        """Return the mean of the values over the quartiles specified."""
        qs = statistics.quartiles(outlier)
        start = qs[start]
        end = qs[end]
        return sum(values[start:end + 1]) / (1 + end - start)


def quartile(values, outlier, quartile, errors):
    return _DataValues(
        statistics.quartile(values, outlier, quartile),
        statistics.errors(values, outlier, errors),
    )


def quartiles(values, outlier, quartile_, errors, axis=1):
    return np.apply_along_axis(
        functools.partial(
            quartile,
            outlier=outlier,
            quartile=quartile_,
            errors=errors
        ),
        axis,
        values
    )


def mean(values, outlier, start, end, errors):
    return _DataValues(
        statistics.mean(values, outlier, start, end),
        statistics.errors(values, outlier, errors),
    )
