import timeit

from typing import List, Callable, Any, Union, Dict, Type, Tuple

from .graphtimer import TimedFunction

SENTINAL: object

TimerFunction = Callable[[], int]
ArgsConvFunction = Callable[..., Tuple[Any, ...]]


class MultiTimer:
    functions: List[TimedFunction]
    timer: Type[timeit.Timer]
    def __init__(self, functions: List[TimedFunction], timer: Type[timeit.Timer]=timeit.Timer) -> None:
        ...

    def build_timer(self,
                    fn: TimedFunction,
                    domain: Any,
                    stmt: str = 'fn(*args)',
                    setup: str = 'pass',
                    timer: Union[TimerFunction, object] = SENTINAL,
                    globals: Union[Dict[str, Any], object] = SENTINAL,
                    args_conv: Union[ArgsConvFunction, object] = SENTINAL
                    ) -> timeit.Timer:
        ...

    def build_timers(self,
                     domain: List[Any],
                     *args: Any,
                     **kwargs: Any
                     ) -> List[List[timeit.Timer]]:
        ...

    def _call(self,
              domain: List[Any],
              repeat: int,
              call: Callable[[timeit.Timer], int],
              *args: Any,
              **kwargs: Any
              ) -> List[List[List[int]]]:
        ...

    def repeat(self,
               domain: List[Any],
               repeat: int,
               number: int,
               *args: Any,
               **kwargs: Any
               ) -> List[List[List[int]]]:
        ...

    def timeit(self,
               domain: List[Any],
               number: int,
               *args: Any,
               **kwargs: Any
               ) -> List[List[int]]:
        ...

    def autorange(self,
                  domain: List[Any],
                  *args: Any,
                  **kwargs: Any
                  ) -> List[List[int]]:
        ...


class TimerNamespaceMeta:
    def __new__(mcs: type, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> TimerNamespace:
        ...


class TimerNamespace:
    TIMER: Type[timeit.Timer]
    MULTI_TIMER: Type[MultiTimer]
    functions: List[TimedFunction]
    multi_timer: MultiTimer
