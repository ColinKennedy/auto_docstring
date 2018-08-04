#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Sphinx-style "Yields" block.'''

# IMPORT LOCAL LIBRARIES
from . import returns_block


class Yields(returns_block.Returns):

    '''The "Yields" block main class.'''

    name = 'yields'
    _info_key = name
