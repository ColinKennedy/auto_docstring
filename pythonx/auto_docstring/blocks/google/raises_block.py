#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
import astroid

# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from ... import environment
from ... import ultisnips_build


class Raises(object):

    label = 'Raises'
    name = 'raises'

    @classmethod
    def draw(cls, info):
        raise_info = info.get('raises')
        if not raise_info:
            return []

        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        parser = ultisnips_build.RecursiveNumberifyParser()
        for raise_object in raise_info:
            type_name = raise_object.exc.func.name
            message = ''
            if cls._include_message():
                message = cls._get_message(raise_object)

            message = environment.drop_trailing_characters(message)
            message = parser.add_conversion(message)

            # TODO : Write message about importance
            message = message[message.index(':') + 1:]

            lines.append(cls._make_line(type_name, message=message))

        return lines

    @staticmethod
    def _make_line(raise_type, message=''):
        indent = environment.get_default_indent()
        if message:
            return '{indent}{raise_type}: {{{number}:{message}!f}}.'.format(
                indent=indent,
                raise_type=raise_type,
                number=common.get_unique_number(),
                message=message,
            )
        else:
            return '{indent}{raise_type}: {{}}.'.format(
                indent=indent, raise_type=raise_type)

    @staticmethod
    def _include_message():
        try:
            return bool(int(os.getenv('AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE', '1')))
        except TypeError:
            return True

    @staticmethod
    def _get_message(node):
        # The first arg of an exception is always the message, unless
        # the exception is some custom object
        #
        packed_message = node.exc.args[0]

        if isinstance(packed_message, astroid.Call):
            packed_message = list(packed_message.func.get_children())[0]
        elif isinstance(packed_message, astroid.Name):
            packed_message = list(packed_message.infer())[0]

        return visit.get_value(packed_message)
