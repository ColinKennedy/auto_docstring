#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ..google import args_block
from ...config import common
from . import mixin


class Args(mixin.SphinxBlockMixin, args_block.Args):
    @staticmethod
    def _make_arg_line(arg):
        return ':param {arg}: {{!f}}.'.format(arg=arg)

    @staticmethod
    def _make_type_line(arg, value):
        if value is not None:
            return ':type {arg}: {{{id_}:{value}!f}}'.format(
                arg=arg,
                id_=common.get_unique_number(),
                value=value,
            )

        return ':type {arg}: {{!f}}'.format(arg=arg)

    @classmethod
    def _build_docstring_lines(cls, lines):
        args = []
        args_types = []

        for arg, value in lines:
            args.append(cls._make_arg_line(arg))
            args_types.append(cls._make_type_line(arg, value))

        return args + args_types
