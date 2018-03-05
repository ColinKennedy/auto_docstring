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

    @classmethod
    def get_block_order(cls):
        if name:
            return common.get_block_order(name)

        return tuple()

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

        cls._add_header(lines)
        cls._add_footer(lines)

        return lines

    @staticmethod
    def get_default_block_order():
        return (
            'args',
            'returns',
            'raises',
            'yields',
        )

    @staticmethod
    def _is_multiline(lines):
        return len(lines) > 1

    @staticmethod
    def _get_spacing():
        try:
            return int(os.getenv('AUTO_DOCSTRING_BLOCK_SPACING', '1'))
        except TypeError:
            return 1

    @classmethod
    def _add_header(cls, lines):
        if cls._is_multiline(lines):
            lines.insert(0, '{}.\n')
        elif not lines:
            lines.insert(0, '{}.')

    @classmethod
    def _add_footer(cls, lines):
        if cls._is_multiline(lines):
            # Add extra newlines, as the footer
            lines.append('')
            lines.append('')

        return lines
