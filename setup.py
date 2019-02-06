#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pyaddepar',
    version='0.5.7',
    packages=find_packages(include=["pyaddepar*"]),
    author='Lobnek Wealth Management',
    author_email='thomas.schmelzer@lobnek.com',
    description='', install_requires=['requests>=2.21.0', 'pandas>=0.24.0']
)
