# graphtimer

This library is based around generating nice graphs for timings.
It's highly modular and provides an interface to quickly and cleanly use modules. 

The high-level interface is the `Plotter` class which takes a timer class as its only argument. The builtin timer is `MultiTimer`, where `TimerNamespace` builds it without you having to. 

From here you have three steps:

1. Time the code by using the timer provided. Usual usage is `repeat`, as `timeit` only times the functions once and skips step 2.
2. Perform the statistical analysis on the timings. Most of the time you'll want to use `min`, which gets the lowest value that isn't an outlier. And shows the error bars from the lowest outlier to Q<sub>3</sub>.
3. Plot the data on the graph. This by default uses `matplotlib` via the `MatPlotLib` class.

```python
import matplotlib.pyplot as plt
from graphtimer import Plotter, TimerNamespace


class ManualListCreation(TimerNamespace):
    def test_comprehension(iterable):
        return [i for i in iterable]

    def test_append(iterable):
        a = []
        append = a.append
        for i in iterable:
            append(i)
        return a


fig, axs = plt.subplots()
(
    Plotter(ManualListCreation)
        .repeat(100, 5, list(range(0, 10001, 1000)), args_conv=range)
        .min()
        .plot(axs)
)
fig.show()
```

## Installation

To install graphtimer, just use pip:

```
$ pip install graphtimer
```