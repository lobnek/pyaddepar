#!/usr/bin/env python

from setuptools import setup, find_packages
from pyaddepar.__init__ import __version__ as version

setup(
    name='pyaddepar',
    version=version,
    packages=find_packages(include=["pyaddepar*"]),
    author='Lobnek Wealth Management',
    author_email='thomas.schmelzer@lobnek.com',
    description='', install_requires=['requests>=2.22.0', 'pandas>=1.0.1']
)
