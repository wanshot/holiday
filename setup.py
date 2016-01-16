#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from bday import (
    __version__,
    __license__,
    __author__,
    __author_email__,
)

__name__ = 'bday'
__url__ = 'https://github.com/wanshot/bday'

__short_description__ = __name__ + ' is a package to generate testdata.'
__long_description__ = open('./README.rst', 'r').read()

__classifiers__ = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development',
]

__keywords__ = [
    'datetime',
    'date',
    'time',
    'calendar',
]

setup(
    name=__name__,
    version=__version__,
    description=__short_description__,
    long_description=__long_description__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    classifiers=__classifiers__,
    keywords=' ,'.join(__keywords__),
    license=__license__,
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
)
