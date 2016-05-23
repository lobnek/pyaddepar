#!./env/bin/python

from setuptools import setup

setup(
    name='pyaddepar',
    version='v0.3.00',
    packages=["pyaddepar"],
    author='Lobnek Wealth Management',
    author_email='thomas.schmelzer@lobnek.com',
    description='', install_requires=['requests>=2.9.1', 'pandas>=0.18.0', 'networkx>=1.11']
)
