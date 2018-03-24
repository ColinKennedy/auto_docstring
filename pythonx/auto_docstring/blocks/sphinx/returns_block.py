#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Sphinx-style "Returns" block.'''

# IMPORT LOCAL LIBRARIES
from ..google import returns_block
from ...config import common
from . import mixin


class Returns(mixin.SphinxBlockMixin, returns_block.Returns):

    '''The "Returns" block main class.'''

    _rtype_label = ':rtype:'
    _item_label = ':returns:'

    @classmethod
    def _make_arg_line(cls):
        return '{item_label} {{!f}}.'.format(item_label=cls._item_label)

    @classmethod
    def _make_type_line(cls, value):
        if value is not None:
            return '{rtype_label} {{{id_}:{value}!f}}'.format(
                rtype_label=cls._rtype_label,
                id_=common.get_unique_number(),
                value=value,
            )

        return '{rtype_label} {{!f}}'.format(rtype_label=cls._type_label, arg=arg)

    @classmethod
    def _build_indented_docstring_lines(cls, lines, indent=''):
        items = []
        items_types = []

        for item in lines:
            items.append(cls._make_arg_line())
            items_types.append(cls._make_type_line(item))

        return items + items_types
