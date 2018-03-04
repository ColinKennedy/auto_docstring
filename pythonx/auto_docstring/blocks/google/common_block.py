#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import abc
import astroid
import inspect
import importlib
import collections
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

    @staticmethod
    def _is_special_type(node):
        return isinstance(node, (astroid.Call, astroid.Attribute, astroid.Name))

    # TODO : Do I actually need info? Remove, if not
    @classmethod
    def _get_special_type_str(cls, obj, info=None):
        inferred_object = list(obj.infer())[0]
        return cls.get_import_path(get_object(inferred_object), info)


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

        # # Note: If we accidentally created a nested list, unpack it
        # # TODO : This condition statment could be cleaned up a bit
        # if len(obj_type) == 1:
        #     obj_type = obj_type[0]

        obj_type = cls._change_type_to_str(*obj_type)

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

        output_types = []
        for subitem in obj:
            if cls._is_special_type(subitem):
                # We'll need to deal with this type later so just ignore it now
                output_types.append(subitem)
                continue

            try:
                container = visit.get_container(subitem)
            except KeyError:
                # subitem was not iterable
                value = visit.get_value(subitem)
                output_types.append(get_type(value))
                continue

            temp_container = []
            for item in cls._expand_types(subitem):
                temp_container.append(item)

            output_types.append(container.__class__(temp_container))

        return output_types

    @classmethod
    def _change_type_to_str(cls, *objs):
        is_flat = len(objs) != 1
        if is_flat:
            output = ''
            objs = reduce_types(objs)
            for obj in objs:
                output = make_options_label(output, make_iterable_label(obj))

            return output

        obj = objs[0]
        if cls._is_special_type(obj):
            return cls._get_special_type_str(obj)

        if not check.is_itertype(obj):
            return get_type_name(obj)

        unique_types = reduce_types(obj)
        return make_iterable_label(unique_types)


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
        module = '.'.join([parent_.name for parent_ in _get_parents(node)])
        module = importlib.import_module(module)
        return getattr(module, parent.name)


def get_container_types():
    return \
        {
            list: list,
            tuple: tuple,
        }


def reduce_types(obj):
    def get_recursive_type(obj):
        if not check.is_itertype(obj):
            yield obj
            return

        item_types = []
        _temp_container = []
        for item in obj:
            inner_item = reduce_types(item)
            if inner_item not in _temp_container:
                _temp_container.append(inner_item)

        yield obj.__class__(_temp_container)

    return list(get_recursive_type(obj))[0]


def make_options_label(*args):
    args = [item for item in args if item]
    if not args:
        return ''
    elif len(args) == 1:
        return args[0]

    return ' or '.join(args)


def make_iterable_label(container):
    def _make_container_label(container, items):
        items = make_options_label(*items)
        container_name = get_type_name(container)

        if items:
            return '{container_name}[{items}]'.format(
                container_name=container_name,
                items=items,
            )
        return container_name

    if not check.is_itertype(container):
        return get_type_name(container)

    # Group every type together
    # so if we have [str], [int], [float], (str, ) then it would look like this
    # {
    #      list: [str, int, float],
    #      tuple: [str]
    # }
    #
    types_ = collections.OrderedDict()

    for item in container:
        if not check.is_itertype(item):
            if item not in types_:
                types_[item] = []
            continue

        item_type = get_type(item)
        types_.setdefault(item_type, [])
        types_[get_type(item)].extend([item_ for item_ in item])

    # Now that every type is grouped together, make text out of each "iterable group"
    items = []
    for type_, subtypes in six.iteritems(types_):
        subtype_names = [get_type_name(subtype) for subtype in subtypes]
        items.append(_make_container_label(type_, subtype_names))

    return _make_container_label(container, items)


def _get_parents(node):
    '''Find every parent of the given AST node.

    This function is useful for Name Nodes, that have a scoped namespace

    Example:
        >>> from collections import OrderedDict
        >>> def foo(bar=OrderedDict):
        >>>     pass
        >>>
        >>> _get_parents(Name.OrderedDict)
        ... # Result: [Module.collections]

    Args:
        node (<astroid Node>): The node to get the parents of.

    Returns:
        list[<asteroid Node>]: The found parents, if any.

    '''
    def __get_parent(node):
        '''Yield parents as they are found, recursively.'''
        try:
            parent = node.parent
        except AttributeError:
            return
            yield
        else:
            yield parent

        for parent in __get_parent(node.parent):
            if parent is not None:
                yield parent

    return list(__get_parent(node))
