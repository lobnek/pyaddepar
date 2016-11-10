#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pyaddepar',
    version='v0.4.00',
    packages=find_packages(include=["pyaddepar*"]),
    author='Lobnek Wealth Management',
    author_email='thomas.schmelzer@lobnek.com',
    description='', install_requires=['requests>=2.9.1', 'pandas>=0.18.0', 'networkx>=1.11']
)
