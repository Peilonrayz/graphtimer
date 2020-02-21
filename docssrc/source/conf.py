import datetime
import pathlib
import sys

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

FILE_PATH = pathlib.Path(__file__).absolute()

# Add documentation for tests
TLD = FILE_PATH.parent.parent.parent
sys.path.insert(0, str(TLD))
config = configparser.ConfigParser()
config.read(TLD / "setup.cfg")

project = "graphtimer"
author = "Peilonrayz"
copyright = f"{datetime.datetime.now().year}, {author}"
release = config.get("src", "version")

master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = []

doctest_global_setup = f"""
import {project}
"""

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
]
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

set_type_checking_flag = True
