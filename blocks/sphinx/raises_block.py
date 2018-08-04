#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..google import raises_block
from ...config import environment
from ...config import common
from . import mixin


class Raises(mixin.SphinxBlockMixin, raises_block.Raises):
    @staticmethod
    def _make_lines(raise_type, message=''):
        # '''Get the docstring representation of the given `raise_type`.

        # Args:
        #     raise_type (str):
        #         The name of the Exception object that was raised in the code.
        #     message (:obj:`str`, optional):
        #         If the Exception was raised with a string message, include it.
        #         If not, just add in an empty "!f" marker.

        # Returns:
        #     str: The output line to create.

        # '''
        indent = environment.get_default_indent()
        if message:
            return [':raises {raise_type}: {{{number}:{message}!f}}.'.format(
                indent=indent,
                raise_type=raise_type,
                number=common.get_unique_number(),
                message=message,
            )]

        return [':raises {raise_type}: {{!f}}.'.format(
            indent=indent, raise_type=raise_type)]
