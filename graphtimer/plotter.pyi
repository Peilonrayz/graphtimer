from typing import List, Any, Union, Tuple, Sequence, Optional, Dict, Type

from .graphtimer import MultiTimerObject, FunctionTimerObject, Graph, TIn, TOut
from .graph import MatPlotLib


Value = Union[int, float]
ErrorInputs = Optional[Sequence[Tuple[int, int]]]
ErrorValues = Optional[List[Tuple[Value, Value]]]
Outlier = Optional[float]
KWArgs = Dict[Any, Any]


class Plotter:
    timer: MultiTimerObject

    def __init__(self, timer: Union[MultiTimerObject, Type[FunctionTimerObject]]) -> None:
        ...

    def timeit(self, number: int, domain: Sequence[Any], *args: Any, **kwargs: Any) -> PlotValues:
        ...

    def repeat(self, repeat: int, number: int, domain: Sequence[Any], *args: Any, **kwargs: Any) -> PlotTimings:
        ...


class _DataSet:
    values: List[Value]

    def __init__(self, values: List[Value]) -> None:
        ...

    def quartile_indexes(self, outlier: Outlier) -> Tuple[int, int, int, int, int]:
        ...

    def errors(self, errors: ErrorInputs, outlier: Outlier) -> ErrorValues:
        ...

    def quartile(self, quartile: int, outlier: Outlier) -> Value:
        ...

    def mean(self, start: int, end: int, outlier: Outlier) -> Value:
        ...


class PlotTimings:
    data: List[List[_DataSet]]
    kwargs: KWArgs

    def __init__(self, data: List[List[List[Value]]], kwargs: KWArgs) -> None:
        ...

    def quartile(self, quartile: int, *, errors: ErrorInputs = None, outlier: Outlier = 1.5) -> PlotValues:
        ...

    def min(self, *, errors: ErrorInputs = ((-1, 3),), outlier: Outlier = 1.5) -> PlotValues:
        ...

    def max(self, *, errors: ErrorInputs = ((1, 5),), outlier: Outlier = 1.5) -> PlotValues:
        ...

    def mean(self, start: int = 0, end: int = 4, *, errors: ErrorInputs = ((1, 3),), outlier: Outlier = 1.5
             ) -> PlotValues:
        ...


class _DataValues:
    value: Value
    errors: ErrorValues

    def __init__(self, value: Value, errors: ErrorValues) -> None:
        ...


class PlotValues:
    data: List[List[_DataValues]]
    kwargs: KWArgs

    def __init__(self, data: List[List[_DataValues]], kwargs: KWArgs) -> None:
        ...

    def plot(self, graph: TIn, graph_lib: Type[Graph[TIn, TOut]] = MatPlotLib, **kwargs: Any) -> List[TOut]:
        ...
