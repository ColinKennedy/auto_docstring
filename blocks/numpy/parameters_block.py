#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ..google import args_block
from ...config import common
from . import mixin


class Parameters(mixin.NumpyMixin, args_block.Args):

    label = 'Parameters'
    name = 'parameters'

    @staticmethod
    def _make_lines(arg, value=''):
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
            line = '{arg} : {{!f}}'.format(arg=arg)
        else:
            line = '{arg} : {{{id_}:{value}!f}}'.format(
                    indent=indent,
                    arg=arg,
                    id_=common.get_unique_number(),
                    value=value)
        second_line = '{indent}{{!f}}.'.format(indent=indent)

        return [line, second_line]
