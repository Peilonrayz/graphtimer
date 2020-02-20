import shutil
from pprint import pprint

import nox


@nox.session(python=["3.4"])
def tests(session):
    session.install(".", "pytest")
    session.run("pytest")


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def coverage(session):
    session.install("coverage>=5.0.0")
    session.install("-e", ".")
    session.install("pytest", "pytest-cov")
    session.run(
        "pytest",
        "--cov=src",
        "--cov-append",
        "--cov-config",
        ".coveragerc",
        "--cov-report",
        "term-missing:skip-covered",
    )
    session.notify("coverage_report")


@nox.session
def coverage_report(session):
    session.install("coverage>=5.0.0")
    session.run("coverage", "html")
    session.notify("coverage_erase")
    session.run("coverage", "report", "--fail-under=100", "--show-missing")


@nox.session
def coverage_erase(session):
    session.install("coverage")
    session.run("coverage", "erase")


FILES = ["src", "tests", "noxfile.py", "noxfile-lint.py", "setup.py"]


@nox.session
def hint(session):
    session.install("isort", "black")
    # session.run('yapf', '--in-place', '--recursive', *FILES)
    session.run("black", *FILES)
    session.run("isort", "--recursive", *FILES)


@nox.session
def lint(session):
    session.install("nox", "vox", "check-manifest")
    # session.run("check-manifest")

    # Delete NOXSESSION so vox can run on CI.
    session.env.pop("NOXSESSION", None)
    session.run("nox", "-r", "-f", "noxfile-lint.py", "--", *session.posargs)


def docs_command(builder):
    return [
        "sphinx-build",
        "-b",
        builder,
        "docssrc/source",
        "docssrc/build/_build/{}".format(builder),
    ]


@nox.session
def docs(session):
    session.notify("docs_test")
    session.notify("docs_build")


@nox.session(python="3.8")
def docs_test(session):
    session.install(".", "sphinx", "sphinx_rtd_theme", "sphinx-autodoc-typehints")
    shutil.rmtree("docssrc/build/", ignore_errors=True)
    session.run(*docs_command("doctest"))
    session.run(*docs_command("linkcheck"))
    session.run(*docs_command("html"))
    shutil.rmtree("docssrc/build/", ignore_errors=True)


@nox.session(python="3.8")
def docs_build(session):
    session.install(".", "sphinx", "sphinx_rtd_theme", "sphinx-autodoc-typehints")
    shutil.rmtree("docs/", ignore_errors=True)
    session.run("sphinx-build", "-b", "html", "docssrc/source", "docs", "-a")
