#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..google import returns_block
from ...config import environment
from ...config import common
from . import mixin


class Returns(mixin.NumpyMixin, returns_block.Returns):

    label = 'Returns'
    name = 'returns'

    @staticmethod
    def _make_item_lines(value=''):
        # '''Get the docstring representation of the given `arg`.

        # Args:
        #     arg (str):
        #         The name of the arg.
        #     value (:obj:`str`, optional):
        #         The default value for this arg. If no value is given,
        #         an unidentified "!f" marker is added, instead.

        # Returns:
        #     str: The output line to create.

        # '''
        indent = environment.get_default_indent()
        if not value:
            line = '{!f}'
        else:
            line = '{{{id_}:{value}!f}}'.format(
                id_=common.get_unique_number(),
                value=value)
        second_line = '{indent}{{!f}}.'.format(indent=indent)

        return [line, second_line]

    @classmethod
    def _build_docstring_lines(cls, lines):
        output = []
        for value in lines:
            output.extend(cls._make_item_lines(value=value))

        return output

    @classmethod
    def draw(cls, info):
        lines = cls._process_args(info)

        if not lines:
            return []

        starting_lines = []

        if info.get('lines'):
            starting_lines = cls.get_starting_lines()

        return starting_lines + cls._build_docstring_lines(lines)
