#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from . import common_block


class Args(common_block.CommonBlock):

    label = 'Args'
    name = 'args'

    @staticmethod
    def _make_line(arg, number=0, value=''):
        indent = common.get_default_indent()
        if value:
            return '{indent}{arg} ({{{id_}|{value}}}, optional): {{}}.'.format(
                indent=indent, arg=arg, id_=number, value=value)
        else:
            return '{indent}{arg} ({{}}): {{}}.'.format(indent=indent, arg=arg)

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

        for index, (arg, value) in enumerate(defaults):
            if cls._is_special_type(value):
                value = cls._get_special_type_str(value, info)
            else:
                value = common_block.get_type_name(visit.get_value(value))

            line = cls._make_line(arg=arg, number=index, value=value)
            lines.append(line)

        if vararg:
            lines.append(cls._make_line(arg='*' + vararg, number=len(defaults), value='tuple'))

        if kwarg:
            lines.append(cls._make_line(arg='**' + kwarg, number=len(defaults) + 1, value='dict'))

        return lines

