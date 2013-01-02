#!/usr/bin/env python
# encoding: utf-8
"""
Installation for command-line ADS to BibDesk

Run::

    setup.py install

and the binary adsbibdesk will be installed into your path.
"""

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='adsbibdesk',
    version='3.1',
    author='Jonathan Sick',
    author_email='jonathansick@mac.com',
    url="http://www.jonathansick.ca/adsbibdesk/",
    description="Add papers from arxiv.org or NASA/SAO ADS to your BibDesk"
                " bibliography.",
    long_description=read('README'),
    keywords="bibtex astronomy",
    classifiers=["Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering :: Astronomy"],
    py_modules=['adsbibdesk'],
    entry_points = {'console_scripts': ['adsbibdesk = adsbibdesk:main']}
)
