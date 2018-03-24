#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..blocks.epydoc import returns_block
from ..blocks.epydoc import args_block
from . import sphinx


class EpydocStyle(sphinx.SphinxStyle):

    _blocks = {
        args_block.Args.name: args_block.Args,
        returns_block.Returns.name: returns_block.Returns,
    }
    name = 'epydoc'

    # TODO : Make sure this works.
    @staticmethod
    def get_default_block_order():
        '''Get the order that blocks will be displayed in.

        This function is used as a fall-back in-case the user did not specify
        their preferred block-order, themselves.

        Returns:
            tuple[str]: The default block order.

        '''
        return (
            'args',
            'returns',
        )
