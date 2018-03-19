#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT STANDARD LIBRARIES
import os
import abc

# IMPORT THIRD-PARTY LIBRARIES
import six

# IMPORT LOCAL LIBRARIES
from ..blocks.google import args_block
from ..blocks.google import raises_block
from ..blocks.google import yields_block
from ..blocks.google import returns_block


@six.add_metaclass(abc.ABCMeta)
class BaseStyle(object):

    _blocks = dict()

    @abc.abstractproperty
    def name():
        return ''

    @staticmethod
    @abc.abstractmethod
    def draw():
        return ''

    @staticmethod
    @abc.abstractmethod
    def get_default_block_order():
        return tuple()

    @classmethod
    def _get_block(cls, block):
        try:
            return cls._blocks[block]
        except KeyError:
            return


class GoogleStyle(BaseStyle):

    name = 'google'
    _blocks = {
        args_block.Args.name: args_block.Args,
        returns_block.Returns.name: returns_block.Returns,
        raises_block.Raises.name: raises_block.Raises,
        yields_block.Yields.name: yields_block.Yields,
    }

    @classmethod
    def draw(cls, info):
        # '''Create a list of docstring lines to create, given some `info`.

        # Args:

        # Returns:
        #     list[str]:
        # '''
        spacing = cls._get_spacing()
        lines = []

        for block_name in cls.get_default_block_order():
            info['lines'] = lines

            block = cls._get_block(block_name)

            if not block:
                raise NotImplementedError(
                    'Block: "{block_name}" has no class for style, "{obj.name}".'
                    ''.format(block_name=block_name, obj=cls))

            block_lines = block.draw(info)
            if block_lines and cls._is_multiline(lines):
                for _ in six.moves.range(spacing):
                    lines.append('')

            lines.extend(block_lines)

        lines = cls._get_header(lines) + lines
        lines += cls._get_footer(lines)

        return lines

    @staticmethod
    def get_default_block_order():
        '''tuple[str]: The default order of blocks for Google-style.'''
        return (
            'args',
            'raises',
            'returns',
            'yields',
        )

    @staticmethod
    def _is_multiline(lines):
        '''bool: If the given lines needs extra spacing.'''
        return len(lines) > 1

    # TODO : Move this to "environment.py"
    @staticmethod
    def _get_spacing():
        '''int: Get the number of newlines to separate each docstring block.'''
        try:
            return int(os.getenv('AUTO_DOCSTRING_BLOCK_SPACING', '1'))
        except TypeError:
            return 1

    @classmethod
    def _get_header(cls, lines):
        '''Recommend the lines to describe the top of the given lines.

        Args:
            lines (list[str]):
                If this arg is not empty, newlines will be added to the bottom
                of the docsrting.

        Returns:
            list[str]: The header for the docstring.

        '''
        if cls._is_multiline(lines):
            return ['{!f}.\n']

        if not lines:
            return ['{!f}.']
        return []

    @classmethod
    def _get_footer(cls, lines):
        '''Create a list of lines to describe the bottom of this docstring.

        Args:
            lines (list[str]):
                If this arg is not empty, newlines will be added to the bottom
                of the docsrting.

        Returns:
            list[str]: The footer of this docstring.

        '''
        if cls._is_multiline(lines):
            return ['', '']
        return []
