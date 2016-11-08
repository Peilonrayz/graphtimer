# graphtimer

Small module to simplify the creation of graphs for timings.

There are two public functions:

 - `time` - A partial builder `timeit.timeit`. Subsequent call will call `timeit` with the string passed as parameter as its setup, automatically adding the import of a function from `__main__`. The function will then be timed by passing the provided parameter, which default to `a`.
 - `flat` - A rudementry function that changes an input to a flattened list.

There is also the class `GraphTimer`. This holds five class variables that are all lists:

 - `functions` - List of functions to passed to the `timeit`s `setup`.
 - `inputs` - List of `functools.partial` wrapped `timeit`s. This is to delay timings.
 - `domain` - List of inputs to test against.
 - `title` - List of graph titles.
 - `colors` - List of colours to use as the line, and area, colours.
