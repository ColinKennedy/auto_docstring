#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The module responsible for printing a Sphinx-style docstrings.'''

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from ..blocks.sphinx import returns_block
from ..blocks.sphinx import raises_block
from ..blocks.sphinx import yields_block
from ..blocks.sphinx import args_block
from . import google


class SphinxStyle(google.GoogleStyle):

    name = 'sphinx'

    _blocks = {
        args_block.Args.name: args_block.Args,
        raises_block.Raises.name: raises_block.Raises,
        returns_block.Returns.name: returns_block.Returns,
        yields_block.Yields.name: yields_block.Yields,
    }

    # TODO : Override spacing rules
    @staticmethod
    def get_spacing():
        # '''int: Get the number of newlines to separate each docstring block.'''
        try:
            return int(os.getenv('AUTO_DOCSTRING_BLOCK_SPACING', '0'))
        except TypeError:
            return 0
