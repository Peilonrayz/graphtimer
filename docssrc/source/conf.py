import datetime

project = 'graphtimer'
author = 'Peilonrayz'
copyright = f'{datetime.datetime.now().year}, {author}'
release = '0.0.0'

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = []

doctest_global_setup = f'''
import {project}
'''

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'sphinx_autodoc_typehints',
]
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

set_type_checking_flag = True
