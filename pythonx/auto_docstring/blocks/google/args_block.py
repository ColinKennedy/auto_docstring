#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from . import common_block
from ... import environment


class Args(common_block.CommonBlock):

    label = 'Args'
    name = 'args'

    @staticmethod
    def _make_line(arg, value=''):
        indent = environment.get_default_indent()
        if value:
            return '{indent}{arg} ({{{id_}:{value}!f}}, optional): {{!f}}.'.format(
                indent=indent,
                arg=arg,
                id_=common.get_unique_number(),
                value=value)
        else:
            return '{indent}{arg} ({{!f}}): {{!f}}.'.format(indent=indent, arg=arg)

    # TODO : Use the logic from common_block.MultiTypeBlock, instead
    @classmethod
    def draw(cls, info):
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
            if common_block.SpecialType.is_valid(value):
                value = common_block.SpecialType(value).as_str(info)
            else:
                value = common_block.get_type_name(visit.get_value(value))

            line = cls._make_line(arg=arg, value=value)
            lines.append(line)

        if vararg:
            lines.append(cls._make_line(arg='*' + vararg, value='tuple'))

        if kwarg:
            lines.append(cls._make_line(arg='**' + kwarg, value='dict'))

        return lines

