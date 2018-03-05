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
from ... import assign_search


class Type(object):
    def __init__(self, obj):
        super(Type, self).__init__()
        self.obj = obj

    def type_contained_in(self, seq):
        return self.get_type() in [item.get_type() for item in seq]

    def get_type(self):
        return get_type(self.obj)

    def __eq__(self, other):
        try:
            return other.obj == self.obj
        except AttributeError:
            return False

    def as_str(self):
        return get_type_name(self.obj)

    def __repr__(self):
        return '{cls_}({obj!r})'.format(
            cls_=self.__class__.__name__,
            obj=self.obj,
        )


class SpecialType(Type):
    def __init__(self, obj):
        super(SpecialType, self).__init__(obj)

    @staticmethod
    def is_valid(node):
        return isinstance(node, (astroid.Call, astroid.Attribute, astroid.Name))

    def as_str(self):
        def search(obj):
            outer_scope = obj.scope()
            return assign_search.find_node_type(outer_scope, name=obj.name)

        inferred_object = list(self.obj.infer())[0]
        if inferred_object == astroid.Uninferable:
            # We could not find a type so search for it (this is a blind search)
            return search(self.obj)

        try:
            # If this was a Named node like foo = [], try to get a type that way
            return get_type_name(visit.get_container_types()[type(inferred_object)])
        except KeyError:
            # Example: tests.google.test_example_google.AdvancedTestCase.test_complex_type_0001
            #          If the inferred object is a astroid.Const, get its type
            #
            try:
                value = visit.get_value(inferred_object)
            except KeyError:
                value = None

            if value is not None:
                return get_type_name(value)

            # If we got to this point, it's because the inferred_object is
            # actually an Attribute or Call object. Try to get the import path
            # for this object
            #
            obj = get_object(inferred_object)
            type_was_not_found = isinstance(obj, six.string_types)
            if type_was_not_found:
                return obj
            return cls.get_import_path(obj, info)


class ContainerType(Type):
    # TODO : Do I need include_type?
    def __init__(self, obj, include_type=True):
        super(ContainerType, self).__init__(obj)
        self.items = []
        self.include_type = include_type

        for subitem in visit.iterate(obj):
            if SpecialType.is_valid(subitem):
                self.items.append(SpecialType(subitem))
                continue

            try:
                container = visit.get_container(subitem)
            except KeyError:
                value = visit.get_value(subitem)
                self.items.append(Type(value))
            else:
                self.items.append(self.__class__(subitem, include_type=True))

    def type_contained_in(self, seq):
        result = super(ContainerType, self).type_contained_in(seq)
        if not result:
            return False

        # If an item in the sequence is a container and that container matches
        # every type in this instance exactly, then we know that it this
        # instance is "in" the container
        #
        current_item_types = [item.get_type() for item in self]
        for item in seq:
            item_types = [subitem.get_type() for subitem in item]
            if item_types == current_item_types:
                return True

        return False

    def as_str(self):
        def make_container_label(container, items_text):
            return '{container}[{items_text}]'.format(
                container=container, items_text=items_text)

        def make_items_text(items):
            return ' or '.join(items)

        items = self._reduce(self.items)
        groups = self._group(items)
        output = []
        for container, subitems in six.iteritems(groups):
            if not subitems:
                output.append(container.as_str())
                continue

            items_text = make_items_text([item.as_str() for item in subitems])
            container_type = visit.get_container_types()[container]
            container_type_name = get_type_name(container_type)

            output.append(make_container_label(container_type_name, items_text))

        output_text = make_items_text(output)

        if self.include_type:
            container_type = visit.get_container_types()[get_type(self.obj)]
            return make_container_label(get_type_name(container_type), output_text)

        return output_text

    def _reduce(self, items):
        def get_recursive_type(obj):
            if not check.is_itertype(obj):
                yield obj
                return

            seen = []

            for item in obj:
                inner_item = self._reduce(item)
                inner_item = check.force_itertype(inner_item)

                if not item.type_contained_in(seen):
                    seen.append(item)

                # for subitem in inner_item:
                #     if not subitem.type_contained_in(seen):
                #         seen.append(subitem)

            yield seen

        return list(get_recursive_type(items))[0]

    def _group(self, items):
        output = collections.OrderedDict()

        for item in items:
            item_type = item.get_type()
            output.setdefault(item_type, [])

            if not check.is_itertype(item):
                output[item_type] = []
                continue

            for subitem in item:
                subitem_type = subitem.get_type()
                if subitem_type not in output[item_type]:
                    output[item_type].append(subitem)

        return output

    def __iter__(self):
        for item in self.items:
            yield item


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

        line = cls._make_line(obj_type)
        lines.append(line)

        return lines

    @abc.abstractproperty
    def _info_key():
        return '_some_key'

    @classmethod
    def _expand_types(cls, obj):
        obj = visit.get_value(obj)
        return ContainerType(obj[0])

    @classmethod
    def _change_type_to_str(cls, objs):
        return objs.as_str()
        # # 'flat' means that we won't include the parent container in the final string
        # is_flat = len(objs) != 1
        # if is_flat:
        #     # Make special types into basic types
        #     objs = [obj for obj in objs]
        #     for index, obj in enumerate(objs):
        #         if SpecialType.is_valid(obj):
        #             objs[index] = cls._get_special_type_str(obj)

        #     # Remove duplicates
        #     objs = reduce_types(objs)

        #     # Now actually create the label
        #     output = ''
        #     for obj in objs:
        #         label = make_iterable_label(obj)
        #         output = make_options_label(output, label)

        #     return output

        # obj = objs[0]
        # if SpecialType.is_valid(obj):
        #     return cls._get_special_type_str(obj)

        # if not check.is_itertype(obj):
        #     return get_type_name(obj)

        # unique_types = reduce_types(obj)
        # return make_iterable_label(unique_types)

    @staticmethod
    def _make_line(obj_type):
        indent = common.get_default_indent()
        return '{indent}{{{obj_type}}}: {{}}.'.format(
            indent=indent,
            obj_type=obj_type,
        )


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
        object or str:
            The node's actual value, in the script.
            If no node value could be found, the name of the object is returned
            as a string.

    '''
    try:
        return node.value
    except AttributeError:
        pass

    try:
        module = '.'.join([parent_.name for parent_ in _get_parents(node)])
        module = importlib.import_module(module)
        return getattr(module, node.name)
    except ImportError:
        return node.name


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


#    @classmethod
#    def _change_type_to_str(cls, *objs):
#        # 'flat' means that we won't include the parent container in the final string
#        is_flat = len(objs) != 1
#        if is_flat:
#            # Make special types into basic types
#            objs = [obj for obj in objs]
#            for index, obj in enumerate(objs):
#                if cls._is_special_type(obj):
#                    objs[index] = cls._get_special_type_str(obj)

#            # Remove duplicates
#            objs = reduce_types(objs)

#            # Now actually create the label
#            output = ''
#            for obj in objs:
#                label = make_iterable_label(obj)
#                output = make_options_label(output, label)

#            return output

#        obj = objs[0]
#        if cls._is_special_type(obj):
#            return cls._get_special_type_str(obj)

#        if not check.is_itertype(obj):
#            return get_type_name(obj)

#        unique_types = reduce_types(obj)
#        return make_iterable_label(unique_types)



#def make_options_label(*args):
#    args = [item for item in args if item]
#    if not args:
#        return ''
#    elif len(args) == 1:
#        return args[0]

#    return ' or '.join(args)


#def make_iterable_label(container):
#    def _make_container_label(container, items):
#        items = make_options_label(*items)
#        container_name = get_type_name(container)

#        if items:
#            return '{container_name}[{items}]'.format(
#                container_name=container_name,
#                items=items,
#            )
#        return container_name

#    if not check.is_itertype(container):
#        return get_type_name(container)

#    # Group every type together
#    # so if we have [str], [int], [float], (str, ) then it would look like this
#    # {
#    #      list: [str, int, float],
#    #      tuple: [str]
#    # }
#    #
#    types_ = collections.OrderedDict()

#    for item in container:
#        if not check.is_itertype(item):
#            if item not in types_:
#                types_[item] = []
#            continue

#        item_type = get_type(item)
#        types_.setdefault(item_type, [])
#        types_[get_type(item)].extend([item_ for item_ in item])

#    # Now that every type is grouped together, make text out of each "iterable group"
#    items = []
#    for type_, subtypes in six.iteritems(types_):
#        subtype_names = [get_type_name(subtype) for subtype in subtypes]
#        items.append(_make_container_label(type_, subtype_names))

#    return _make_container_label(container, items)

