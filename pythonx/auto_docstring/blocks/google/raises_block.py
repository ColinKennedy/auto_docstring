#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
import astroid

# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from . import common_block
from ... import environment
from ... import ultisnips_build


class Raises(common_block.CommonBlock):

    label = 'Raises'
    name = 'raises'

    @classmethod
    def draw(cls, info):
        raise_info = info.get('raises', [])
        raise_info = cls._filter_unnamed(raise_info)

        if not raise_info:
            return []

        starting_line = '{}:'.format(cls.label)
        lines = [starting_line]

        parser = ultisnips_build.RecursiveNumberifyParser()
        for raise_object in raise_info:
            type_name = cls._get_exception_name(raise_object)

            message = ''
            if cls._include_message():
                message = cls._get_message(raise_object)

            message = environment.drop_trailing_characters(message)
            # TODO : Add '%d' and all the other ones, too
            # Also, add significance for this block of text. Why is it needed? etc
            message = message.replace('%s', '{}')
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
            return '{indent}{raise_type}: {{!f}}.'.format(
                indent=indent, raise_type=raise_type)

    @staticmethod
    def _include_message():
        try:
            return bool(int(os.getenv('AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE', '1')))
        except TypeError:
            return True

    @staticmethod
    def _get_exception_name(node):
        try:
            # If the user wrote the exception like `raise ValueError()`
            return node.exc.func.name
        except AttributeError:
            pass

        try:
            # If the user wrote the exception like `raise ValueError`
            return node.exc.name
        except AttributeError:
            return ''

    @staticmethod
    def _get_message(node):
        # The first arg of an exception is always the message, unless
        # the exception is some custom object
        #
        try:
            packed_message = node.exc.args[0]
        except AttributeError:
            # If node.exc has no args, it means the user wrote the exception
            # with no message, like this: `raise ValueError`
            return ''
        except IndexError:
            # If args is empty, it means the user wrote the exception like this:
            # `raise ValueError`
            return ''

        if isinstance(packed_message, astroid.Call):
            packed_message = list(packed_message.func.get_children())[0]
        elif isinstance(packed_message, astroid.Name):
            packed_message = list(packed_message.infer())[0]

        return visit.get_value(packed_message)

    @classmethod
    def _filter_unnamed(cls, raise_info):
        return [info for info in raise_info if cls._get_exception_name(info)]
