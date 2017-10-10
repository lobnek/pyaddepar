#!/usr/bin/env python3
import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


#sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

#sys.path.insert(0, "/pylobnek/pylobnek")
sys.path.insert(0, "/pyaddepar/")

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.viewcode'
]


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'pyaddepar'
copyright = '2017, Lobnek Wealth Management'
author = 'Lobnek Wealth Management'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '3.2'
# The full version, including alpha/beta/rc tags.
release = '3.2.0'



# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'



# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'


# Output file base name for HTML help builder.
htmlhelp_basename = 'pyaddepar'




