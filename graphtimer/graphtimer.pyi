from typing import Any, Tuple, Sequence, List, Callable, Optional, ClassVar, Generic, TypeVar

import typing_extensions

CATEGORY10: Tuple[str, ...]
CATEGORY20: Tuple[str, ...]
CATEGORY20b: Tuple[str, ...]
CATEGORY20c: Tuple[str, ...]


def flat(i: Any) -> Sequence[Any]:
    ...


TimedFunction = Callable[..., Any]


class MultiTimerObject(typing_extensions.Protocol):
    functions: List[TimedFunction]

    def repeat(self,
               domain: Sequence[Any],
               repeat: int,
               number: int,
               *args: Any,
               **kwargs: Any
               ) -> List[List[List[int]]]:
        ...

    def timeit(self,
               domain: Sequence[Any],
               number: int,
               *args: Any,
               **kwargs: Any
               ) -> List[List[int]]:
        ...

    def autorange(self,
                  domain: Sequence[Any],
                  *args: Any,
                  **kwargs: Any
                  ) -> List[List[int]]:
        ...


class FunctionTimerObject(typing_extensions.Protocol):
    multi_timer: ClassVar[MultiTimerObject]


TIn = TypeVar('TIn', contravariant=True)
TOut = TypeVar('TOut')


class Graph(typing_extensions.Protocol, Generic[TIn, TOut]):
    def graph(self,
              graph: TIn,
              data: List[List[Any]],
              domain: List[Any],
              *,
              functions: Optional[List[TimedFunction]] = None,
              colors: Tuple[str, ...] = CATEGORY10,
              title: Optional[str]=None,
              legend: bool=True,
              error: bool=True
              ) -> List[TOut]:
        ...