#!/usr/bin/env python
from setuptools import setup, find_packages

version = '0.0.2'
description = 'Time code execution and graph results'
with open('README.md', 'r') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
]

install_requires = []

test_requires = []

extra_requires = {
    'base': [
        'matplotlib',
    ]
}

setup(
    name='graphtimer',
    version=version,
    description=description,
    long_description=long_description,
    author='Peilonrayz',
    author_email='peilonrayz@gmail.com',
    url='https://github.com/Peilonrayz/graphtimer',
    license='MIT',
    keywords='timer graph performance',
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extra_requires,
)
