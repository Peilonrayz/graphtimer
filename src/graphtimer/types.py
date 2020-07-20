from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

import typing_extensions

TimedFunction = Callable[..., Any]


class MultiTimerObject(typing_extensions.Protocol):
    functions: List[TimedFunction]

    def repeat(
        self, domain: Sequence[Any], repeat: int, number: int, *args: Any, **kwargs: Any
    ) -> List[List[List[int]]]:
        ...

    def timeit(
        self, domain: Sequence[Any], number: int, *args: Any, **kwargs: Any
    ) -> List[List[int]]:
        ...

    def autorange(
        self, domain: Sequence[Any], *args: Any, **kwargs: Any
    ) -> List[List[int]]:
        ...


class FunctionTimerObject(typing_extensions.Protocol):
    multi_timer: ClassVar[MultiTimerObject]


TIn = TypeVar("TIn", contravariant=True)
TOut = TypeVar("TOut")


class Graph(typing_extensions.Protocol, Generic[TIn, TOut]):
    def graph(
        self,
        graph: TIn,
        values: List[float],
        errors: List[float],
        domain: List[Any],
        *,
        functions: Optional[List[TimedFunction]] = None,
        colors: Tuple[str, ...] = (),
        title: Optional[str] = None,
        legend: bool = True,
        error: bool = True
    ) -> List[TOut]:
        ...
