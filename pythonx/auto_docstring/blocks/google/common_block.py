#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import abc
import inspect
import __builtin__

# IMPORT THIRD-PARTY LIBRARIES
import six

# IMPORT LOCAL LIBRARIES
from ... import visit
from ... import common
from ...core import check
from ...core import grouping


@six.add_metaclass(abc.ABCMeta)
class CommonBlock(object):
    label = 'Header label'

    @staticmethod
    @abc.abstractmethod
    def draw(info):
        return []

    @abc.abstractproperty
    def name():
        return '_unique_id'

    @classmethod
    def get_starting_line(cls):
        return '{}:'.format(cls.label)

    @staticmethod
    def get_import_path(obj, info=None):
        def is_builtin_type(obj):
            objects = []
            for attr in dir(__builtin__):
                attr = getattr(__builtin__, attr)
                objects.append(attr)
            objects = tuple((obj_ for obj_ in objects if inspect.isclass(obj_)))
            return obj in objects

        class_type = obj

        if not inspect.isclass(obj):
            class_type = obj.__class__

        if inspect.isbuiltin(obj) or is_builtin_type(class_type):
            return class_type.__name__

        name = obj.__name__
        parent = inspect.getmodule(obj).__name__
        return '<{parent}.{name}>'.format(parent=parent, name=name)


@six.add_metaclass(abc.ABCMeta)
class MultiTypeBlock(CommonBlock):
    @classmethod
    def draw(cls, info):
        expected_object = info.get(cls._info_key)

        if not expected_object:
            return []

        lines = []
        indent = ''

        if info.get('lines'):
            lines = [cls.get_starting_line()]
            indent = common.get_default_indent()

        obj_type = cls._expand_types(expected_object)
        obj_type = cls._change_type_to_str(obj_type)

        line = '{indent}{{{obj_type}}}: {{}}.'.format(
            indent=indent,
            obj_type=obj_type,
        )

        lines.append(line)

        return lines

    @abc.abstractproperty
    def _info_key():
        return '_some_key'

    @classmethod
    def _expand_types(cls, obj):
        if not check.is_itertype(obj):
            yield get_type(obj)
            return

        for item in obj:
            # If item is a astroid.List or some other iterable type, expand it
            value = visit.get_value(item)
            yield value
            # _temp_container = [item_ for item_ in value]
            # for index, subitem in enumerate(_temp_container):
            #     _temp_container[index] = cls._expand_types(subitem)

            # yield value.__class__(_temp_container)

    @classmethod
    def _change_type_to_str(cls, obj):
        # if not check.is_itertype(obj):
        #     return obj

        all_types = []
        for container in obj:
            _temp_container = [item_ for item_ in container]
            for index, item in enumerate(_temp_container):
                _temp_container[index] = type(visit.get_value(item))

            # Make each type unique without losing order
            _temp_container = grouping.uniquify_list(_temp_container)

            # Now convert each type to a string representation
            _temp_container = [get_type_name(_item) for _item in _temp_container]
            container = container.__class__(_temp_container)

        args = ' or '.join(container)
        return '{container}[{args}]'.format(
            container=get_type_name(container),
            args=args)


def get_type(obj):
    return obj.__class__


def get_type_name(obj):
    if not inspect.isclass(obj):
        obj = obj.__class__

    return obj.__name__


def get_object(node):
    '''Find the underlying object of a given astroid Node.

    If the given node is actually a Name, like how OrderedDict is a Name for
    <collections.OrderedDict>, find its actual object and return it.

    Args:
        node (<astroid Node>): Some node to process.

    Returns:
        The node's actual value, in the script.

    '''
    try:
        return node.value
    except AttributeError:
        parent = list(node.infer())[0]
        module = '.'.join([parent_.name for parent_ in _get_parents(parent)])
        module = importlib.import_module(module)
        return getattr(module, parent.name)

