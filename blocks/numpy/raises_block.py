#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ..google import raises_block
from ...config import common
from . import mixin


class Raises(mixin.NumpyMixin, raises_block.Raises):

    label = 'Raises'
    name = 'raises'

    @staticmethod
    def _make_lines(raise_type, message=''):
        # '''Get the docstring representation of the given `raise_type`.

        # Args:
        #     raise_type (str):
        #         The name of the raise_type.
        #     message (:obj:`str`, optional):
        #         The default message for this raise_type. If no message is given,
        #         an unidentified "!f" marker is added, instead.

        # Returns:
        #     str: The output line to create.

        # '''
        indent = environment.get_default_indent()
        if message:
            second_line = '{indent}{{{id_}:{message}!f}}.'.format(
                indent=indent,
                id_=common.get_unique_number(),
                message=message)
        else:
            second_line = '{indent}{{!f}}.'.format(indent=indent)

        return [raise_type, second_line]
