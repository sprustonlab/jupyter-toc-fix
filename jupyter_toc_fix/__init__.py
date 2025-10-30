"""
jupyter-toc-fix
===============

Automatically configures jupyter_contrib_nbextensions with useful extensions and
fixes the Table of Contents (TOC2) positioning issue.

During installation, this package:
1. Installs nbextensions to the environment
2. Enables the nbextensions configurator
3. Activates 5 useful extensions (toc2, collapsible_headings, hide_input_all,
   init_cell, codefolding)
4. Applies a CSS fix for TOC positioning

References:
- https://stackoverflow.com/questions/75621836
- https://github.com/ipython-contrib/jupyter_contrib_nbextensions/issues/1568
"""

__version__ = '0.2.0'
