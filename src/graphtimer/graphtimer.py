import collections
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

__all__ = [
    "CATEGORY10",
    "CATEGORY20",
    "CATEGORY20b",
    "CATEGORY20c",
    # Helpers
    "flat",
]

CATEGORY10: Tuple[str, ...] = tuple(
    "#1f77b4 #ff7f0e #2ca02c #d62728 #9467bd #8c564b #e377c2 #7f7f7f #bcbd22 #17becf".split()
)
CATEGORY20: Tuple[str, ...] = tuple(
    "#1f77b4 #aec7e8 #ff7f0e #ffbb78 #2ca02c #98df8a #d62728 #ff9896 #9467bd #c5b0d5 "
    "#8c564b #c49c94 #e377c2 #f7b6d2 #7f7f7f #c7c7c7 #bcbd22 #dbdb8d #17becf #9edae5".split()
)
CATEGORY20b: Tuple[str, ...] = tuple(
    "#393b79 #5254a3 #6b6ecf #9c9ede #637939 #8ca252 #b5cf6b #cedb9c #8c6d31 #bd9e39 "
    "#e7ba52 #e7cb94 #843c39 #ad494a #d6616b #e7969c #7b4173 #a55194 #ce6dbd #de9ed6".split()
)
CATEGORY20c: Tuple[str, ...] = tuple(
    "#3182bd #6baed6 #9ecae1 #c6dbef #e6550d #fd8d3c #fdae6b #fdd0a2 #31a354 #74c476 "
    "#a1d99b #c7e9c0 #756bb1 #9e9ac8 #bcbddc #dadaeb #636363 #969696 #bdbdbd #d9d9d9".split()
)


def flat(i: Any) -> Sequence[Any]:
    if hasattr(i, "flat"):
        return i.flat
    if not isinstance(i, collections.Iterable) or isinstance(i, str):
        return [i]
    list_ = i
    while True:
        if any(
            not isinstance(item, collections.Iterable) or isinstance(item, str)
            for item in list_
        ):
            return list_
        list_ = [item for iterable in list_ for item in iterable]
