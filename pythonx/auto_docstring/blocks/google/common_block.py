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

        # Note: If we accidentally created a nested list, unpack it
        # TODO : This condition statment could be cleaned up a bit
        if len(obj_type) == 1:
            obj_type = obj_type[0]

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
        obj = visit.get_value(obj)

        if not check.is_itertype(obj):
            return get_type(obj)

        container = visit.get_container(obj)
        temp_container = []
        for subitem in obj:
            value = cls._expand_types(subitem)

            if value:
                temp_container.append(value)

            # # Drill down one level deeper if we catch an instance
            # if not inspect.isclass(value):
            #     value = visit.get_value(subitem)

            # temp_container.append(value)

        return container.__class__(temp_container)

    @classmethod
    def _change_type_to_str(cls, obj):
        all_types = []
        for container in obj:
            if not check.is_itertype(container):
                all_types.append(get_type_name(container))
                continue

            # Make each element unique
            container = container.__class__(grouping.uniquify(container))

            # Convert the types down to just their names
            container = cls._change_type_to_str(container)
            all_types.append(container)

        # Make the final types unique, too
        all_types = grouping.uniquify(all_types)

        args = ' or '.join(all_types)
        return '{obj}[{args}]'.format(
            obj=get_type_name(obj),
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

