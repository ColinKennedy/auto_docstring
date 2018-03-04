#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import abc
import inspect
import __builtin__

# IMPORT THIRD-PARTY LIBRARIES
import six

# IMPORT LOCAL LIBRARIES
from ... import common
from ...core import check


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
        obj_type = cls._format_types(obj_type)

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
        if check.is_itertype(obj):
            if len(obj) == 1:
                return cls.get_import_path(obj[0])

            _temp_container = []
            for item in obj:
                item = cls._expand_types(item)
                item_type = cls.get_import_path(item)
                _temp_container.append(item_type)

            obj = obj.__class__(_temp_container)
            return obj

        return obj

    @classmethod
    def _format_types(cls, obj):
        if not check.is_itertype(obj):
            return obj

        items = []
        for item in obj:
            item = cls._format_types(item)
            if item not in items:
                items.append(item)

        return ' or '.join(items)