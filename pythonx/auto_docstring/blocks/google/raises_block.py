#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Google-style "Raises:" block.'''

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
import astroid

# IMPORT LOCAL LIBRARIES
from . import common_block
from ...config import common
from ...parsing import visit
from ...parsing import numberify
from ...config import environment


class Raises(common_block.CommonBlock):

    '''The "Raises:" block main class.'''

    label = 'Raises'
    name = 'raises'

    # TODO : Remove "get_starting_line" and replace it with "get_starting_lines"
    @classmethod
    def get_starting_lines(cls):
        return ['{}:'.format(cls.label)]

    @classmethod
    def draw(cls, info):
        '''Create the docstring lines to represent the given `info`.

        Args:
            info (dict[str, list]):
                Each of the different "raise" statements and their values.

        Returns:
            list[str]: The lines to create.

        '''
        raise_info = info.get('raises', [])
        raise_info = cls._filter_unnamed(raise_info)

        if not raise_info:
            return []

        lines = cls.get_starting_lines()

        parser = numberify.RecursiveNumberifyParser()
        for raise_object in raise_info:
            type_name = cls._get_exception_name(raise_object)

            message = ''
            if cls._include_message():
                message = cls._get_message(raise_object)

            message = environment.drop_trailing_characters(message)
            # Also, add significance for this block of text. Why is it needed? etc
            message = cls._replace_format_markers(message)
            message = parser.add_conversion(message)

            # TODO : Write message about importance
            message = message[message.index(':') + 1:]

            lines.extend(cls._make_lines(type_name, message=message))

        return lines

    @staticmethod
    def _make_lines(raise_type, message=''):
        '''Get the docstring representation of the given `raise_type`.

        Args:
            raise_type (str):
                The name of the Exception object that was raised in the code.
            message (:obj:`str`, optional):
                If the Exception was raised with a string message, include it.
                If not, just add in an empty "!f" marker.

        Returns:
            str: The output line to create.

        '''
        indent = environment.get_default_indent()
        if message:
            return ['{indent}{raise_type}: {{{number}:{message}!f}}.'.format(
                indent=indent,
                raise_type=raise_type,
                number=common.get_unique_number(),
                message=message,
            )]

        return ['{indent}{raise_type}: {{!f}}.'.format(
            indent=indent, raise_type=raise_type)]

    # TODO : Move this to environment.py
    @staticmethod
    def _include_message():
        '''bool: Whether to add raised messages to their docstrings or not.'''
        try:
            return bool(int(os.getenv('AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE', '1')))
        except TypeError:
            return True

    @staticmethod
    def _get_exception_name(node):
        '''Get the name of the given `node`.

        Args:
            node (`astroid.Call` or `astroid.Name`):
                The raised object to get the name of.

        Returns:
            str: The name of the given `node`.

        '''
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
        '''Find the message of the given `node`, if any.

        Not all raised exceptions are given messages, for example
        raise ValueError() and raise ValueError are just as valid as
        raise ValueError('foo'). But if it does have a message, find it.

        Args:
            node (`astroid.Call` or `astroid.Name`):
                The raised object to get the message of.

        Returns:
            str: The found message, if any.

        '''
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
        '''Remove all bare raise statements.

        Example:
            # This "raise" will be removed
            >>> try:
            ...    None['foo']
            >>> except TypeError:
            ...    raise

            # This "raise" will not be removed
            >>> try:
            ...    None['foo']
            >>> except TypeError:
            ...    raise TypeError

        Args:
            raise_info (list[`astroid.Call` or `astroid.Name`]):
                The raised objects that may or may not contain bare exceptions.

        Returns:
            list[`astroid.Call` or `astroid.Name`]: The raised, named objects.

        '''
        return [info for info in raise_info if cls._get_exception_name(info)]

    @staticmethod
    def _replace_format_markers(text):
        return text.replace('%s', '{}').replace('%d', '{}').replace('%r', '{}').replace('%f', '{}')
