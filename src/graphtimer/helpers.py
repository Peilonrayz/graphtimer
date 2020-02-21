import numpy as np


def quartiles(values, outlier=1.5):
    quartiles = np.linspace(0, len(values) - 1, num=5).round().astype("int").tolist()

    if outlier is not None:
        if outlier < 0:
            raise ValueError("outlier should be non-negative.")
        q75, q25 = np.percentile(values, [75, 25])
        iqr = outlier * (q75 - q25)
        low = q25 - iqr
        high = q75 + iqr
        quartiles[0] = np.argmax(values >= low)
        quartiles[4] = len(values) - np.argmax(values[::-1] <= high) - 1
    return np.array(tuple(quartiles) + (-1, 0))


def errors(values, outlier, errors):
    """Returns tuples containing the quartiles wanted."""
    if errors is None:
        return None
    qs = quartiles(values, outlier)
    errors = np.array(errors)
    return values[qs[errors.flatten()]].resize(errors.shape)


def quartile(values, outlier, quartile):
    """Return the value of the quartile provided."""
    qs = quartiles(values, outlier)
    return values[qs[quartile]]


def mean(values, outlier, start, end):
    """Return the mean of the values over the quartiles specified."""
    qs = quartiles(outlier)
    start = qs[start]
    end = qs[end]
    return np.mean(values[start : end + 1])
