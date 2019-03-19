from typing import List, Any, Tuple, Optional, Iterator, Sequence

from .graphtimer import CATEGORY10, TimedFunction, TIn, TOut, Graph
from .plotter import _DataValues


class MatPlotLib(Graph[TIn, TOut]):
    @staticmethod
    def error_line(results: Sequence[Tuple[int, int, int]]) -> Iterator[Tuple[int, int, int]]:
        ...

    def _graph_times(self,
                     graph: TIn,
                     data: List[List[_DataValues]],
                     domain: List[Any],
                     colors: Tuple[str, ...],
                     error: bool,
                     fmt: str
                     ) -> Iterator[TOut]:
        ...

    def graph(self,
              graph: TIn,
              data: List[List[_DataValues]],
              domain: List[Any],
              *,
              functions: Optional[List[TimedFunction]] = None,
              colors: Tuple[str, ...] = CATEGORY10,
              title: Optional[str] = None,
              legend: bool = True,
              error: bool = True,
              x_label: Optional[str] = 'Input',
              y_label: Optional[str] = 'Time [s]',
              fmt: str = '-'
              ) -> List[TOut]:
        ...