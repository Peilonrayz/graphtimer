import inspect
import timeit
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from .types import TimedFunction

SENTINAL: object = object()
PASSABLE_KEYWORDS = {"_i"}

TimerFunction = Callable[[], int]
ArgsConvFunction = Callable[..., Tuple[Any, ...]]


class MultiTimer:
    """Interface to timeit.Timer to ease timing over multiple functions."""

    functions: List[TimedFunction]
    timer: Type[timeit.Timer]

    def __init__(
        self, functions: List[TimedFunction], timer: Type[timeit.Timer] = timeit.Timer,
    ) -> None:
        self.timer = timer
        self.functions = functions

    def build_timer(
        self,
        fn: TimedFunction,
        domain: Any,
        stmt: str = "fn(*args)",
        setup: str = "pass",
        timer: Union[TimerFunction, object] = SENTINAL,
        globals: Union[Dict[str, Any], object] = SENTINAL,
        args_conv: Union[ArgsConvFunction, object] = SENTINAL,
        **extras,
    ) -> timeit.Timer:
        """Build a timeit.Timer"""
        if not isinstance(domain, tuple):
            domain = (domain,)
        if args_conv is not SENTINAL:
            kwargs = {}
            try:
                sig = inspect.signature(args_conv)
            except (TypeError, ValueError):
                pass
            else:
                for param in sig.parameters.values():
                    if (
                        param.name in PASSABLE_KEYWORDS
                        and param.name in extras
                        and param.kind == inspect.Parameter.KEYWORD_ONLY
                    ):
                        kwargs[param.name] = extras[param.name]

            domain = args_conv(*domain, **kwargs)
            if not isinstance(domain, tuple):
                domain = (domain,)

        if globals is SENTINAL:
            globals = {}
        else:
            globals = globals.copy()
        globals.update({"fn": fn, "args": domain})

        # print(f'{self.timer}({stmt!r}, {setup!r}, {timer!r}, {globals!r})')

        if timer is SENTINAL:
            timer = timeit.default_timer

        return self.timer(stmt, setup, timer, globals=globals)

    def build_timers(
        self, domain: List[Any], *args: Any, **kwargs: Any,
    ) -> List[List[timeit.Timer]]:
        """Build multiple timers from various inputs and functions"""
        return [
            [self.build_timer(fn, dom, *args, **kwargs) for fn in self.functions]
            for dom in domain
        ]

    def _call(
        self,
        domain: List[Any],
        repeat: int,
        call: Callable[[timeit.Timer], int],
        *args: Any,
        **kwargs: Any,
    ) -> List[List[List[int]]]:
        """Helper function to generate timing data."""
        if len(domain) == 0:
            raise ValueError("domain must have at least one argument.")

        output = [[[] for _ in domain] for _ in self.functions]
        for repeat_num in range(repeat):
            functions = self.build_timers(domain, *args, **kwargs, _i=repeat_num)
            for j, fns in enumerate(functions):
                for i, fn in enumerate(fns):
                    output[i][j].append(call(fn))
        return output

    def repeat(
        self, domain: List[Any], repeat: int, number: int, *args: Any, **kwargs: Any,
    ) -> List[List[List[int]]]:
        """Interface to timeit.Timer.repeat. `domain` is the values to pass to the functions."""
        return self._call(domain, repeat, lambda f: f.timeit(number), *args, **kwargs)

    def timeit(
        self, domain: List[Any], number: int, *args: Any, **kwargs: Any,
    ) -> List[List[int]]:
        """Interface to timeit.Timer.timeit. `domain` is the values to pass to the functions."""
        return [
            [value[0] for value in values]
            for values in self.repeat(domain, 1, number, *args, **kwargs)
        ]

    def autorange(
        self, domain: List[Any], *args: Any, **kwargs: Any
    ) -> List[List[int]]:
        """Interface to timeit.Timer.autorange. `domain` is the values to pass to the functions."""
        return [
            [value[0] for value in values]
            for values in self._call(
                domain, 1, lambda f: f.autorange(), *args, **kwargs
            )
        ]


class TimerNamespaceMeta(type):
    """Convenience class to ease creation of a MultiTimer."""

    def __new__(
        mcs: type, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]
    ) -> "TimerNamespace":
        if "functions" in attrs:
            raise TypeError("FunctionTimers cannot define `functions`")
        if "multi_timer" in attrs:
            raise TypeError("FunctionTimers cannot define `multi_timer`")

        ret: TimerNamespace = super().__new__(mcs, name, bases, attrs)
        functions = [v for k, v in attrs.items() if k.startswith("test")]
        ret.functions = functions
        ret.multi_timer = ret.MULTI_TIMER(functions, ret.TIMER)
        return ret


class TimerNamespace(metaclass=TimerNamespaceMeta):
    """Convenience class to ease creation of a MultiTimer."""

    functions: List[TimedFunction]
    multi_timer: MultiTimer

    TIMER: Type[timeit.Timer] = timeit.Timer
    MULTI_TIMER: Type[MultiTimer] = MultiTimer
