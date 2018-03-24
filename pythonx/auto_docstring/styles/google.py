#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The module responsible for printing a Google-style docstring for functions.'''

# IMPORT STANDARD LIBRARIES
import os
import abc
import sys

# IMPORT THIRD-PARTY LIBRARIES
import six

# IMPORT LOCAL LIBRARIES
from ..blocks.google import args_block
from ..blocks.google import raises_block
from ..blocks.google import yields_block
from ..blocks.google import returns_block


# TODO : Double check that this has everything
@six.add_metaclass(abc.ABCMeta)
class BaseStyle(object):

    '''An abstract class that is used to create a docstring style.'''

    _blocks = dict()
    # TODO : Replace uses of {!f} with this attribute
    marker = '{!f}'

    @abc.abstractproperty
    def name(self):
        '''str: A unique name for this class.'''
        return ''

    @staticmethod
    @abc.abstractmethod
    def draw(info):
        '''str: The final, auto-generated docstring.'''
        return ''

    @staticmethod
    @abc.abstractmethod
    def get_default_block_order():
        '''Get the order that blocks will be displayed in.

        This function is used as a fall-back in-case the user did not specify
        their preferred block-order, themselves.

        Returns:
            tuple[str]: The default block order.

        '''
        return tuple()

    @classmethod
    def _get_block(cls, block):
        '''Get the class used for the given `block` name.

        Args:
            block (str): The name of a registered block class.

        Returns:
            :class:`auto_docstring.blocks.google.common_block` or NoneType:
                The found block.

        '''
        try:
            return cls._blocks[block]
        except KeyError:
            return


class GoogleStyle(BaseStyle):

    '''The class that is responsible for creating Google-style docstrings.

    Reference:
        auto_docstring docstrings are written in Google-style. More examples
        can be found here: http://www.sphinx-doc.org/en/master/ext/example_google.html

    '''

    name = 'google'
    _blocks = {
        args_block.Args.name: args_block.Args,
        returns_block.Returns.name: returns_block.Returns,
        raises_block.Raises.name: raises_block.Raises,
        yields_block.Yields.name: yields_block.Yields,
    }

    @classmethod
    def get_max_spacing(cls, lines):
        if lines and cls._is_multiline(lines):
            return sys.maxint
        return 0

    # TODO : Clean up vararg. It should only be str
    # TODO : Clean up kwarg. It should only be str
    # TODO : Possibly pass FunctionDef into info?
    # TODO : Come back to this docstring and write about NotImplementedError
    #        after there are some unittests for user-defined blocks
    #
    # TODO : Make note about how info is mutated by this function
    #
    @classmethod
    def draw(cls, info):
        '''Create a list of docstring lines to create, given some `info`.

        Args:
            info (dict[str, list[str] or `astroid.NodeNG` or NoneType):
                The information to draw.

                'vararg' (str or NoneType):
                    The name of the `*args` function parameter.
                'returns' (list[`astroid.NodeNG`]):
                    The object(s) that this function returns.
                'kwarg': (NoneType or str):
                    The name of the `**kwargs` function parameter.
                'defaults' (list[tuple[str, `astroid.NodeNG`]]):
                    The name and default value of the function parameters.
                'in': (`astroid.Module` or NoneType):
                    The root module that defined the `astroid.FunctionDef`.

        Raises:
            NotImplementedError:
                If a block that was selected to be drawn has no block-class.

        Returns:
            list[str]: The generated docstring lines.

        '''
        blocks = []

        info.setdefault('lines', [])

        # Collect the blocks to draw and their contents
        for block_name in cls.get_default_block_order():
            block = cls._get_block(block_name)

            if not block:
                raise NotImplementedError(
                    'Block: "{block_name}" has no class for style, "{obj.name}".'
                    ''.format(block_name=block_name, obj=cls))

            block_lines = block.draw(info)

            if block_lines:
                info['lines'] += block_lines
                blocks.append((block, block_lines))
                continue

        # Now add spacing for each of the drawn blocks
        lines = []
        blocks_len = len(blocks)
        for index, (block, block_lines) in enumerate(blocks):
            lines.extend(block_lines)

            is_last_block = index + 1 == len(blocks)

            if is_last_block:
                continue

            spacing = min(cls.get_max_spacing(block_lines), block.get_spacing())

            for _ in six.moves.range(spacing):
                lines.append('')

        lines = cls._get_header(lines) + lines
        lines += cls._get_footer(lines)

        return lines

    # TODO : Make sure this works.
    @staticmethod
    def get_default_block_order():
        '''Get the order that blocks will be displayed in.

        This function is used as a fall-back in-case the user did not specify
        their preferred block-order, themselves.

        Returns:
            tuple[str]: The default block order.

        '''
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
            return ['{marker}.\n'.format(marker=cls.marker)]

        if not lines:
            return ['{marker}.'.format(marker=cls.marker)]
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
