#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ..google import args_block
from ...config import common
from . import mixin


class Args(mixin.SphinxBlockMixin, args_block.Args):

    _parameter_label = ':param'
    _type_label = ':type'

    @classmethod
    def _make_arg_line(cls, arg):
        return '{parameter} {arg}: {{!f}}.'.format(
            parameter=cls._parameter_label, arg=arg)

    @classmethod
    def _make_type_line(cls, arg, value):
        if value is not None:
            return '{type_label} {arg}: {{{id_}:{value}!f}}'.format(
                type_label=cls._type_label,
                arg=arg,
                id_=common.get_unique_number(),
                value=value,
            )

        return '{type_label} {arg}: {{!f}}'.format(type_label=cls._type_label, arg=arg)

    @classmethod
    def _build_docstring_lines(cls, lines):
        args = []
        args_types = []

        for arg, value in lines:
            args.append(cls._make_arg_line(arg))
            args_types.append(cls._make_type_line(arg, value))

        return args + args_types
