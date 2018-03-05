#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT STANDARD LIBRARIES
from ... import visit
from ... import common
from . import common_block


class Args(common_block.CommonBlock):

    label = 'Args'
    name = 'args'

    @classmethod
    def draw(cls, info):
        args = info.get('args', [])
        defaults = info.get('defaults', [])
        vararg = info.get('vararg', '')
        kwarg = info.get('kwarg', '')

        if not args and not defaults and not vararg:
            return []

        indent = common.get_default_indent()
        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        for arg in args:
            line = '{indent}{arg} ({{}}): {{}}.'.format(indent=indent, arg=arg)
            lines.append(line)

        for index, (arg, value) in enumerate(defaults):
            if cls._is_special_type(value):
                value = cls._get_special_type_str(value, info)
            else:
                value = common_block.get_type_name(visit.get_value(value))

            line = '{indent}{arg} ({{{id_}|{value}}}, optional): {{}}.'.format(
                indent=indent,
                arg=arg,
                id_=index,
                value=value,
            )
            lines.append(line)

        if vararg:
            lines.append(
                '{indent}{arg} ({{{id_}|{value}}}, optional): {{}}.'.format(
                    indent=indent,
                    arg='*' + vararg,
                    id_=len(defaults),
                    value='tuple',
            ))

        if kwarg:
            lines.append(
                '{indent}{arg} ({{{id_}|{value}}}, optional): {{}}.'.format(
                    indent=indent,
                    arg='**' + kwarg,
                    id_=len(defaults) + 1,
                    value='dict',
            ))

        return lines

