#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT STANDARD LIBRARIES
from ... import common
from . import common_block


class Args(common_block.CommonBlock):

    label = 'Args'
    name = 'args'

    @classmethod
    def draw(cls, info):
        args = info.get('args', [])
        defaults = info.get('defaults', [])

        if not args and not defaults:
            return []

        indent = common.get_default_indent()
        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        for arg in args:
            line = '{indent}{arg} ({{}}): {{}}.'.format(indent=indent, arg=arg)
            lines.append(line)

        for arg, value in defaults:
            print('asdffsd', value, cls.get_import_path(value))
            line = '{indent}{arg} ({{{value}}}, optional): {{}}.'.format(
                indent=indent,
                arg=arg,
                value=cls.get_import_path(value, info),
            )
            lines.append(line)

        return lines

