#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Sphinx-style "Yields" block.'''

# IMPORT LOCAL LIBRARIES
from ..google import yields_block
from . import mixin


class Yields(yields_block.Yields, mixin.SphinxBlockMixin):

    '''The "Yields" block main class.'''
