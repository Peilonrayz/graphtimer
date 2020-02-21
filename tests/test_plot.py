import pathlib

import helpers.functions as se_code
import matplotlib.pyplot as plt
import numpy as np
import pytest
from graphtimer import Plotter, flat

ALL_TESTS = True


@pytest.mark.skipif(
    pathlib.Path("static/figs/reverse.png").exists() and ALL_TESTS,
    reason="Output image already exists",
)
def test_reverse_plot():
    fig, axs = plt.subplots()
    axs.set_yscale("log")
    axs.set_xscale("log")
    (
        Plotter(se_code.Reverse)
        .repeat(10, 10, np.logspace(0, 3), args_conv=lambda i: " " * int(i))
        .min()
        .plot(axs, title="Reverse", fmt="-o")
    )
    fig.savefig("static/figs/reverse.png")
    fig.savefig("static/figs/reverse.svg")


@pytest.mark.skipif(
    pathlib.Path("static/figs/graipher.png").exists() and ALL_TESTS,
    reason="Output image already exists",
)
def test_graipher_plot():
    fig, axs = plt.subplots()
    (
        Plotter(se_code.Graipher)
        .repeat(2, 1, [i / 10 for i in range(10)])
        .min()
        .plot(axs, title="Graipher", fmt="-o")
    )
    fig.savefig("static/figs/graipher.png")
    fig.savefig("static/figs/graipher.svg")


@pytest.mark.skipif(
    pathlib.Path("static/figs/peilonrayz.png").exists() and ALL_TESTS,
    reason="Output image already exists",
)
def test_peilonrayz_plot():
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    p = Plotter(se_code.Peilonrayz)
    axis = [
        ("Range", {"args_conv": range}),
        ("List", {"args_conv": lambda i: list(range(i))}),
        ("Unoptimised", {"args_conv": se_code.UnoptimisedRange}),
    ]
    for graph, (title, kwargs) in zip(iter(flat(axs)), axis):
        (
            p.repeat(100, 5, list(range(0, 10001, 1000)), **kwargs)
            .min(errors=((-1, 3), (-1, 4)))
            .plot(graph, title=title)
        )
    fig.savefig("static/figs/peilonrayz.png")
    fig.savefig("static/figs/peilonrayz.svg")
