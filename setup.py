#!/usr/bin/env python

from setuptools import setup, find_packages
from pyaddepar.__init__ import __version__ as version

# read the contents of your README file
with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyaddepar',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=find_packages(include=["pyaddepar*"]),
    author='Lobnek Wealth Management',
    url='https://github.com/lobnek/pyaddepar',
    author_email='thomas.schmelzer@lobnek.com',
    description='Utility code for working with Addepar', install_requires=['requests>=2.22.0', 'pandas>=0.25.3']
)
