from typing import TYPE_CHECKING, Any, Iterator, List, Optional, Sequence, Tuple

from .graphtimer import CATEGORY10
from .types import Graph, TimedFunction, TIn, TOut

if TYPE_CHECKING:
    from .plotter import _DataValues


class MatPlotLib:
    def _graph_times(
        self,
        graph: TIn,
        values: List[List["_DataValues"]],
        errors: List[Any],
        domain: List[Any],
        colors: Tuple[str, ...],
        error: bool,
        fmt: str,
    ) -> Iterator[TOut]:
        for values, errors, color in zip(values, errors, colors):
            if error and not any(e is None for e in errors):
                errors = zip(*errors)
                for error in errors:
                    lower, upper = zip(*error)
                    graph.fill_between(
                        domain, upper, lower, facecolor=color, edgecolor=None, alpha=0.1
                    )
            yield graph.plot(domain, values, fmt, color=color)[0]

    def graph(
        self,
        graph: TIn,
        values: List[List["_DataValues"]],
        errors: List[Any],
        domain: List[Any],
        *,
        functions: Optional[List[TimedFunction]] = None,
        colors: Tuple[str, ...] = CATEGORY10,
        title: Optional[str] = None,
        legend: bool = True,
        error: bool = True,
        x_label: Optional[str] = "Input",
        y_label: Optional[str] = "Time [s]",
        fmt="-"
    ):
        lines = list(
            self._graph_times(graph, values, errors, domain, colors, error, fmt)
        )
        if x_label is not None:
            graph.set_xlabel(x_label)
        if y_label is not None:
            graph.set_ylabel(y_label)
        if title is not None and hasattr(graph, "set_title"):
            graph.set_title(title)
        if legend and functions is not None and hasattr(graph, "legend"):
            legend = [
                getattr(fn, "__qualname__", None) or fn.__name__ for fn in functions
            ]
            graph.legend(lines, legend, loc=0)
        return lines
