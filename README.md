# graphtimer

Small module to simplify the creation of graphs for timings.

There are two public functions:

 - `time` - A helper function to `timeit.timeit`. It changes the argument layout so the command is the last parameter, with the default `'fn(a)'`. This is as in most my timings I've only needed one function. I also pass `a` as I normally time against a single amount.
 - `flat` - This is a rudementry function that changes an input to a flatterned list.

There is also the class `GraphTimer`. This holds five class variables that are all lists:

 - `functions` - List of functions to passed to the `timeit`s `setup`.
 - `inputs` - List of `functools.partial` wrapped `timeit`s. This is to delay timings.
 - `domain` - List of inputs to test against.
 - `title` - List of graph titles.
 - `colors` - List of colours to use as the line, and area, colours.
