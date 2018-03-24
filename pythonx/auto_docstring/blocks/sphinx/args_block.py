#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ..google import args_block
from ...config import common


class Args(args_block.Args):
    @staticmethod
    def _make_arg_line(arg):
        indent = environment.get_default_indent()
        return '{indent}:param {arg}: {{!f}}.'.format(
            indent=indent,
            arg=arg,
        )

    @staticmethod
    def _make_type_line(value):
        indent = environment.get_default_indent()
        if value is not None:
            return '{indent}:type {{{id_}:{value}!f}}: {{!f}}'.format(
                indent=indent,
                id_=common.get_unique_number(),
                value=value,
            )

        return '{indent}:type {{!f}}: {{!f}}'.format(
            indent=indent,
        )

    @classmethod
    def _build_docstring_lines(cls, lines):
        args = []
        args_types = []

        for arg, value in lines:
            args.append(cls._make_arg_line(arg))
            args_types.append(cls._make_type_line(value))

        return args + args_types
