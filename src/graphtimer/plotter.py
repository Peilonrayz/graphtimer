from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

import numpy as np

from . import helpers
from .graph import MatPlotLib
from .types import FunctionTimerObject, Graph, MultiTimerObject, TIn, TOut

Value = Union[int, float]
ErrorInputs = Optional[Sequence[Tuple[int, int]]]
ErrorValues = Optional[List[Tuple[Value, Value]]]
Outlier = Optional[float]
KWArgs = Dict[Any, Any]


class PlotValues:
    """Thin interface to Graph.graph."""

    values: List[float]
    errors: List[float]
    kwargs: KWArgs

    def __init__(
        self, values: List[float], errors: List[float], kwargs: KWArgs
    ) -> None:
        self.values = values
        self.errors = errors
        self.kwargs = kwargs

    def plot(
        self, graph: TIn, graph_lib: Type[Graph[TIn, TOut]] = MatPlotLib, **kwargs: Any
    ) -> List[TOut]:
        g = graph_lib()
        return g.graph(
            graph,
            self.values,
            self.errors,
            self.kwargs.pop("domain"),
            functions=self.kwargs.pop("functions"),
            **kwargs,
        )


class PlotTimings:
    """Thin interface over _DataSet"""

    data: List[List[List[Value]]]
    kwargs: KWArgs

    def __init__(self, data: List[List[List[Value]]], kwargs: KWArgs) -> None:
        self.data = data
        self.kwargs = kwargs

    def quartile(
        self,
        quartile: int,
        *,
        errors: ErrorInputs = None,
        outlier: Outlier = 1.5,
        axis: int = 2,
    ) -> PlotValues:
        """Interface to _DataSet.quartile and errors. Returns a PlotValues."""
        return PlotValues(
            np.apply_along_axis(helpers.quartile, axis, self.data, outlier, quartile,),
            np.apply_along_axis(
                helpers.errors, axis, self.data, outlier, np.array(errors),
            ),
            self.kwargs,
        )

    def min(
        self, *, errors: ErrorInputs = ((-1, 3),), outlier: Outlier = 1.5
    ) -> PlotValues:
        """Return the Q1 value and show the error from Q-1 Q3."""
        return self.quartile(0, errors=errors, outlier=outlier)

    def max(
        self, *, errors: ErrorInputs = ((1, 5),), outlier: Outlier = 1.5
    ) -> PlotValues:
        """Return the Q4 value and show the error from Q1 Q5."""
        return self.quartile(4, errors=errors, outlier=outlier)

    def mean(
        self,
        start: int = 0,
        end: int = 4,
        *,
        errors: ErrorInputs = ((1, 3),),
        outlier: Outlier = 1.5,
        axis=2,
    ) -> PlotValues:
        """Interface to _DataSet.mean and errors. Returns a PlotValues."""
        return PlotValues(
            np.apply_along_axis(helpers.mean, axis, self.data, outlier, start, end,),
            np.apply_along_axis(
                helpers.errors, axis, self.data, outlier, np.array(errors),
            ),
            self.kwargs,
        )


class Plotter:
    """Interface to the timer object. Returns objects made to ease usage."""

    timer: MultiTimerObject

    def __init__(
        self, timer: Union[MultiTimerObject, Type[FunctionTimerObject]]
    ) -> None:
        self.timer = getattr(timer, "multi_timer", timer)

    def timeit(
        self, number: int, domain: Sequence[Any], *args: Any, **kwargs: Any
    ) -> PlotValues:
        """Interface to self.timer.timeit. Returns a PlotValues."""
        return self.repeat(1, number, domain, *args, **kwargs).min(errors=None)

    def repeat(
        self, repeat: int, number: int, domain: Sequence[Any], *args: Any, **kwargs: Any
    ) -> PlotTimings:
        """Interface to self.timer.repeat. Returns a PlotTimings."""
        return PlotTimings(
            self.timer.repeat(domain, repeat, number, *args, **kwargs),
            {"functions": self.timer.functions, "domain": domain},
        )
