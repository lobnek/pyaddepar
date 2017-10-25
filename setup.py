#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pyaddepar',
    version='v0.5.00',
    packages=find_packages(include=["pyaddepar*"]),
    author='Lobnek Wealth Management',
    author_email='thomas.schmelzer@lobnek.com',
    description='', install_requires=['requests>=2.12.0', 'pandas>=0.20.0']
)
