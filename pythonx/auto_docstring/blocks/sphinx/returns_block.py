#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Sphinx-style "Returns" block.'''

# IMPORT LOCAL LIBRARIES
from ..google import returns_block
from ...config import common
from . import mixin


class Returns(mixin.SphinxBlockMixin, returns_block.Returns):

    '''The "Returns" block main class.'''

    @staticmethod
    def _make_arg_line():
        return ':returns: {{!f}}.'.format()

    @staticmethod
    def _make_type_line(value):
        if value is not None:
            return ':rtype: {{{id_}:{value}!f}}'.format(
                id_=common.get_unique_number(),
                value=value,
            )

        return ':rtype: {{!f}}'.format(arg=arg)

    @classmethod
    def _build_indented_docstring_lines(cls, lines, indent=''):
        items = []
        items_types = []

        for item in lines:
            items.append(cls._make_arg_line())
            items_types.append(cls._make_type_line(item))

        return items + items_types
