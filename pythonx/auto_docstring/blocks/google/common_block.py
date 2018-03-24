#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO : Just had an idea. Why not change the gross "if X.is_valid(obj): return X(obj)
#        into a single classmethod? That'd look way better and potentially be
#        easier to loop over
#
'''The classes and functions needed to parse the types of all astroid nodes.

This module does most of the heavy-lifting for args return-types. It can
parse functions within functions, infer an object's type, and even recursively
traverse imported modules to get an object's type.

'''

# IMPORT STANDARD LIBRARIES
import abc
import os

# IMPORT THIRD-PARTY LIBRARIES
import six

# IMPORT LOCAL LIBRARIES
from ...config import environment
from ...parsing import visit
from ...core import check
from . import common_type


@six.add_metaclass(abc.ABCMeta)
class CommonBlock(object):

    '''An abstract class used to implement a Google-style block.

    Attributes:
        label (str): The block display text.

    '''

    label = 'Header label'

    @staticmethod
    @abc.abstractmethod
    def draw(info):
        '''Create the docstring lines to represent the given `info`.

        Args:
            info (dict[str]):
                The parsed AST node whose type needs to be found and then
                converted into a string.

        Returns:
            list[str]: The lines to create.

        '''
        return []

    @abc.abstractproperty
    def name(self):
        '''str: A unique name to use to identify this block-type.'''
        return '_unique_id'

    @classmethod
    def get_starting_lines(cls):
        '''list[str]: Get the label used for the top of this block.'''
        return ['{}:'.format(cls.label)]

    @staticmethod
    def get_spacing():
        return

    @staticmethod
    def get_spacing():
        '''int: Get the number of newlines to separate each docstring block.'''
        try:
            return int(os.getenv('AUTO_DOCSTRING_BLOCK_SPACING', '1'))
        except TypeError:
            return 1

    @staticmethod
    def _expand_types(obj, include_type=False):
        r'''Wrap the given `obj` with a specific docstring-class wrapper.

        Args:
            obj (`astroid.NodeNG`):
                Some node to wrap.
            include_type (bool, optional):
                If True and `obj` is a container of some kind, for example
                a list of strs, then `obj` will be printed like "list[str]".
                If False, `obj` would be printed as just "str".
                This parameter is used primarily mainly for keeping return-types
                from accidentally printing its container-type twice when
                the container is nested.
                Default is False.

        Returns:
            `SpecialType` or `ComprehensionContainerType` or `ContainerType` \
                    or `IterableType` or `Type`: .
                The wrapped type.

        '''
        if common_type.SpecialType.is_valid(obj):
            return common_type.SpecialType(obj)

        obj = visit.get_value(obj)

        if common_type.ComprehensionContainerType.is_valid(obj):
            return common_type.ComprehensionContainerType(obj)

        if common_type.ContainerType.is_valid(obj):
            return common_type.ContainerType(obj)

        if check.is_itertype(obj):
            return common_type.IterableType(obj, include_type=include_type)

        return common_type.Type(obj)

    @staticmethod
    def _change_type_to_str(*objs):
        '''Create the full string of all return-types for the given `objs`.

        Args:
            *objs (list[:class:`auto_docstring.blocks.google.common_block.Type`]):
                The types to change into strings.

        Returns:
            str: The final set of return types for the given objects. This string
                 will be added to the auto-generated docstrings, directly.

        '''
        items = []
        for item in [obj.as_str() for obj in objs]:
            if item not in items:
                items.append(item)

        return common_type.make_items_text(items)


@six.add_metaclass(abc.ABCMeta)
class MultiTypeBlock(CommonBlock):

    '''The base-class used to create "Returns" and "Yields" blocks.'''

    _info_key = '_some_key'
    name = 'multitype_base_block'

    @classmethod
    def _process_args(cls, info):
        expected_object = info.get(cls._info_key)

        if not expected_object:
            return []

        indent = ''

        # Check if I need this if-statement
        if info.get('lines'):
            indent = environment.get_default_indent()

        info['indent'] = indent

        obj_types = cls._expand_types(expected_object)
        type_info_as_str = cls._change_type_to_str(*obj_types)

        return [type_info_as_str]

    @classmethod
    def _build_indented_docstring_lines(cls, lines, indent=''):
        return [cls._make_line(line, indent=indent) for line in lines]

    @classmethod
    def draw(cls, info):
        # '''Create the docstring lines to represent the given `info`.

        # Note:
        #     If no data is found for cls._info_key, this method will return
        #     an empty list.

        # Args:
        #     info (dict[str, list[`astroid.NodeNG`]]):
        #         The parsed AST node whose type needs to be found and then
        #         converted into a string.

        # Returns:
        #     list[str]: The lines to create.

        # '''
        lines = cls._process_args(info)

        if not lines:
            return []

        starting_lines = []

        if info.get('lines'):
            starting_lines = cls.get_starting_lines()

        return starting_lines + cls._build_indented_docstring_lines(lines, info.get('indent', ''))

    @staticmethod
    def _make_line(obj_type, indent):
        '''Create the docstring line for the given input.

        Args:
            indent (str): The amount of space to add to the docstring block.
            obj_type (str): The type of the object. Example: "tuple[str]", "bool".

        Returns:
            str: The created docstring line.

        '''
        return '{indent}{{:{obj_type}!f}}: {{!f}}.'.format(
            indent=indent,
            obj_type=obj_type,
        )
