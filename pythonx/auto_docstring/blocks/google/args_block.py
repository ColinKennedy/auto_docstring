#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The block class and functions needed to print a Google-style "Args:" block.'''

# IMPORT LOCAL LIBRARIES
from . import common_block
from ...config import common
from ...config import environment


class Args(common_block.CommonBlock):

    '''The "Args:" block main class.'''

    label = 'Args'
    name = 'args'

    @staticmethod
    def _make_line(arg, value=''):
        '''Get the docstring representation of the given `arg`.

        Args:
            arg (str):
                The name of the arg.
            value (:obj:`str`, optional):
                The default value for this arg. If no value is given,
                an unidentified "!f" marker is added, instead.

        Returns:
            str: The output line to create.

        '''
        indent = environment.get_default_indent()
        if value:
            return '{indent}{arg} ({{{id_}:{value}!f}}, optional): {{!f}}.'.format(
                indent=indent,
                arg=arg,
                id_=common.get_unique_number(),
                value=value)

        return '{indent}{arg} ({{!f}}): {{!f}}.'.format(indent=indent, arg=arg)

    # TODO : Use the logic from common_block.MultiTypeBlock, instead
    @classmethod
    def draw(cls, info):
        '''Create the docstring lines to represent the given `info`.

        Args:
            info (dict[str, list or str]):
                The args, default-args, `*`, and `**` parameters to process.
                If nothing is given, this method will return an empty list.

        Returns:
            list[str]: The lines to create.

        '''
        args = info.get('args', [])
        defaults = info.get('defaults', [])
        vararg = info.get('vararg', '')
        kwarg = info.get('kwarg', '')

        if not args and not defaults and not vararg:
            return []

        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        for arg in args:
            line = cls._make_line(arg)
            lines.append(line)

        for arg, value in defaults:
            obj_types = cls._expand_types(value, include_type=True)
            value = cls._change_type_to_str(obj_types)

            line = cls._make_line(arg=arg, value=value)
            lines.append(line)

        if vararg:
            lines.append(cls._make_line(arg='*' + vararg, value='tuple'))

        if kwarg:
            lines.append(cls._make_line(arg='**' + kwarg, value='dict'))

        return lines
