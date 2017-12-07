"""Tikz magic"""
__version__ = '0.0.1'

from .tikz import TikzMagic

def load_ipython_extension(ipython):
    ipython.register_magics(TikzMagic)