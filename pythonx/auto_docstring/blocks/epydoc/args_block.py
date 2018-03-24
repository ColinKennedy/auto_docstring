#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..sphinx import args_block


class Args(args_block.Args):

    _parameter_label = '@param'
    _type_label = '@type'

    @classmethod
    def _build_docstring_lines(cls, lines):
        args = []

        for arg, value in lines:
            args.append(cls._make_arg_line(arg))
            args.append(cls._make_type_line(arg, value))

        return args
