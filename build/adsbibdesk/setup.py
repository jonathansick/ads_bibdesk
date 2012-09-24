#!/usr/bin/env python
# encoding: utf-8
"""
Installation for command-line ADS to BibDesk

Run:
    setup.py install

and the binary adsbibdesk will be installed into your path.

2012-09-23 - Created by Jonathan Sick
"""

from setuptools import setup

setup(
    name='adsbibdesk',
    version='3.0.2',
    py_modules=['adsbibdesk'],
    entry_points = {
            'console_scripts': ['adsbibdesk = adsbibdesk:main']
        }
)
