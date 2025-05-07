#!/usr/bin/env python3
# flake8: noqa
""" Top-level module.

Portrait (Gleckler) plotting API.
"""
from pkg_resources import DistributionNotFound, get_distribution

from .portrait import portrait_plot

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    __version__ = 'unknown'  # pragma: no cover

__all__ = ['portrait_plot']
