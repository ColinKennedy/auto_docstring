#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Sphinx-style "Returns" block.'''

# IMPORT LOCAL LIBRARIES
from ..google import returns_block
from . import mixin


class Returns(returns_block.Returns, mixin.SphinxBlockMixin):

    '''The "Returns" block main class.'''
