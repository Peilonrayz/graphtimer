import timeit

SENTINAL = object()


class MultiTimer:
    """Interface to timeit.Timer to ease timing over multiple functions."""
    def __init__(self, functions, timer=timeit.Timer):
        self.timer = timer
        self.functions = functions

    def build_timer(self, fn, domain, stmt='fn(*args)', setup='pass', timer=SENTINAL, globals=SENTINAL,
                    args_conv=SENTINAL):
        """Build a timeit.Timer"""
        if not isinstance(domain, tuple):
            domain = domain,
        if args_conv is not SENTINAL:
            domain = args_conv(*domain)

        if globals is SENTINAL:
            globals = {}
        else:
            globals = globals.copy()
        globals.update({'fn': fn, 'args': domain})

        # print(f'{self.timer}({stmt!r}, {setup!r}, {timer!r}, {globals!r})')

        if timer is SENTINAL:
            timer = timeit.default_timer

        return self.timer(stmt, setup, timer, globals=globals)

    def build_timers(self, domain, *args, **kwargs):
        """Build multiple timers from various inputs and functions"""
        return [
            [
                self.build_timer(fn, dom, *args, **kwargs)
                for fn in self.functions
            ]
            for dom in domain
        ]

    def _call(self, domain, repeat, call, *args, **kwargs):
        """Helper function to generate timing data."""
        if len(domain) == 0:
            raise ValueError('domain must have at least one argument.')

        functions = self.build_timers(domain, *args, **kwargs)
        output = [[[] for _ in domain] for _ in functions[0]]
        for _ in range(repeat):
            for j, fns in enumerate(functions):
                for i, fn in enumerate(fns):
                    output[i][j].append(call(fn))
        return output

    def repeat(self, domain, repeat, number, *args, **kwargs):
        """Interface to timeit.Timer.repeat. `domain` is the values to pass to the functions."""
        return self._call(domain, repeat, lambda f: f.timeit(number), *args, **kwargs)

    def timeit(self, domain, number, *args, **kwargs):
        """Interface to timeit.Timer.timeit. `domain` is the values to pass to the functions."""
        return [
            [value[0] for value in values]
            for values in self.repeat(domain, 1, number, *args, **kwargs)
        ]

    def autorange(self, domain, *args, **kwargs):
        """Interface to timeit.Timer.autorange. `domain` is the values to pass to the functions."""
        return [
            [value[0] for value in values]
            for values in self._call(domain, 1, lambda f: f.autorange(), *args, **kwargs)
        ]


class FunctionTimerMeta(type):
    """Convenience class to ease creation of a MultiTimer."""
    def __new__(mcs, name, bases, attrs):
        if 'functions' in attrs:
            raise TypeError('FunctionTimers cannot define `functions`')
        if 'multi_timer' in attrs:
            raise TypeError('FunctionTimers cannot define `multi_timer`')

        ret: FunctionTimer = super().__new__(mcs, name, bases, attrs)
        functions = [v for k, v in attrs.items() if k.startswith('test')]
        ret.functions = functions
        ret.multi_timer = ret.MULTI_TIMER(functions, ret.TIMER)
        return ret


class FunctionTimer(metaclass=FunctionTimerMeta):
    """Convenience class to ease creation of a MultiTimer."""
    TIMER = timeit.Timer
    MULTI_TIMER = MultiTimer
