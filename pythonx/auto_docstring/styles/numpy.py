#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..blocks.numpy import parameters_block
from ..blocks.numpy import returns_block
from ..blocks.numpy import raises_block
from . import google


class NumpyStyle(google.GoogleStyle):

    name = 'numpy'

    _blocks = {
        parameters_block.Parameters.name: parameters_block.Parameters,
        raises_block.Raises.name: raises_block.Raises,
        returns_block.Returns.name: returns_block.Returns,
        # yields_block.Yields.name: yields_block.Yields,
    }

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
            'parameters',
            'raises',
            'returns',
            # 'yields',
        )
