"""Asymptote magic"""
__version__ = '0.0.1'

from .asymptote import AsymptoteMagic

def load_ipython_extension(ipython):
    ipython.register_magics(AsymptoteMagic)