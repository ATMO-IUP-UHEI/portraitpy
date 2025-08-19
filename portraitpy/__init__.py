#!/usr/bin/env python3
# flake8: noqa
""" Top-level module.

Portrait (Gleckler) plotting API.
"""
from importlib.metadata import version

from .portrait import portrait_plot

__version__ = version(__name__)

__all__ = ['portrait_plot']
