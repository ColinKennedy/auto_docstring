#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from . import common_block


class Raises(object):

    label = 'Raises'
    name = 'raises'

    @classmethod
    def draw(cls, info):
        empty_raises = [None, None]
        raise_info = info.get('raises', empty_raises)
        if raise_info == empty_raises:
            return []

        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        for index, (raise_type, message) in enumerate(raise_info):
            if cls._include_message():
                lines.append(cls._make_line(raise_type, number=index, message=message))
            else:
                lines.append(cls._make_line(raise_type, number=index))

        return lines

    @staticmethod
    def _make_line(raise_type, number=0, message=''):
        indent = common.get_default_indent()
        if message:
            return '{indent}{raise_type}: {{{number}|{message}}}.'.format(
                indent=indent, raise_type=raise_type, number=number, message=message)
        else:
            return '{indent}{raise_type}: {{}}.'.format(
                indent=indent, raise_type=raise_type)

    @staticmethod
    def _include_message():
        try:
            return bool(int(os.getenv('AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE', '1')))
        except TypeError:
            return True
