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

# IMPORT AUTO-DOCSTING LIBRARIES
import auto_docstring

# IMPORT LOCAL LIBRARIES
from ... import visit
from ...core import check
from ... import environment
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

    # TODO : Check if info is necessary. If not, remove it
    def as_str(self, info=None):
        # See if the object is a built-in, callable object
        # - if it is, return that type's name
        # - if not and it is a callable object, like another function
        #   then get its return-type signature
        #     - If it cannot get the callable object's signature, return the
        #       name of the callable object, in <>s
        # - If the object is local to this module that we are making a docstring
        #   for, then our last possible-effort would be to try to use astroid to
        #   "infer" what that object's type would be, and return it
        #
        found_type = process_types(self.obj)
        if found_type is not None:
            return found_type

        try:
            inferred_object = list(self.obj.infer())[0]
        except astroid.NameInferenceError:
            # We couldn't infer the type so, assuming self.obj is astroid.Name,
            # return the name, directly
            #
            return self.obj.name

        if inferred_object == astroid.Uninferable:
            # We could not find a type so search for it (this is a blind search)
            try:
                return self.search(self.obj)
            except ValueError:
                try:
                    return self.obj.name
                except AttributeError:
                    return

        try:
            # If this was a Named node like foo = [], try to get a type that way
            return get_type_name(visit.get_container_types()[type(inferred_object)])
        except KeyError:
            pass

        # TODO : This entire section seems like something that would be useful
        #        to other classes. Possibly move, to another location

        # Example: tests.google.test_example_google.AdvancedTestCase.test_complex_type_0001
        #          If the inferred object is a astroid.Const, get its type
        #
        try:
            value = visit.get_value(inferred_object)
        except KeyError:
            value = None

        if value is not None:
            return get_type_name(value)

        # If the type is obvious (example: a Compare object will be a bool)
        # Then just get the Python type and use it
        #
        try:
            return get_type_name(visit.get_type(inferred_object))
        except ValueError:
            pass

        # If we got to this point, it's because the inferred_object is
        # actually an Attribute or Call object. Try to get the import path
        # for this object
        #
        obj = get_object(inferred_object)
        type_was_not_found = isinstance(obj, six.string_types)
        if type_was_not_found:
            return obj
        return self.get_import_path(obj, info)

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

        return make_third_party_label('{parent}.{name}'.format(parent=parent, name=name))

    @staticmethod
    def search(obj):
        outer_scope = obj.scope()
        try:
            found_type = assign_search.find_node_type(outer_scope, name=obj.name)
        except RuntimeError:
            raise ValueError('Obj: "{obj}" was not assigned.'.format(obj=obj))
        return get_type_name(found_type)


class ContainerType(Type):
    def __init__(self, obj, include_type=True):
        super(ContainerType, self).__init__(obj)
        self.items = []
        self.include_type = include_type

        for subitem in visit.iterate(obj):
            # If it's a Name or Call object and its type needs to be inferred
            if SpecialType.is_valid(subitem):
                self.items.append(SpecialType(subitem))
                continue

            # If it's a pairwise container, like a dict
            if MappingContainerType.is_valid(subitem):
                self.items.append(MappingContainerType(subitem))
                continue

            if ComprehensionContainerType.is_valid(subitem):
                self.items.append(ComprehensionContainerType(subitem))
                continue

            # If the type is obvious (example: a Compare object will be a bool)
            # Then just get the Python type and use it
            #
            try:
                subitem_type = visit.get_type(subitem)
                self.items.append(Type(subitem_type))
                continue
            except ValueError:
                pass

            # If subitem is a list, tuple, or other iterable container
            try:
                visit.get_container(subitem)
                self.items.append(self.__class__(subitem, include_type=True))
                continue
            except KeyError:
                pass

            # If it's not an object type or a container, then try to find that
            # value of subitem, directly
            #
            value = visit.get_value(subitem)
            self.items.append(Type(value))

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
        def _get_container_type_name(container):
            container_type = visit.get_container_types()[container]
            return get_type_name(container_type)

        items = self._reduce(self.items)
        groups = self._group(items)
        output = []
        for container, subitems in six.iteritems(groups):
            try:
                # If the container is nested, get its type name
                container_type_name = _get_container_type_name(container)
            except KeyError:
                # If this happens, it just means that the container is not
                # nested (example: a list[str]). `container`, in this case,
                # is just <astroid.Str> so we can get get its type, directly
                #
                container_type_name = get_type_name(container)

            if not subitems:
                output.append(container_type_name)
                continue

            items_text = make_items_text([item.as_str() for item in subitems])
            container_label = make_container_label(container_type_name, items_text)
            output.append(container_label)

        output_text = make_items_text(output)

        if self.include_type:
            return make_container_label(
                _get_container_type_name(get_type(self.obj)),
                output_text,
            )

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

            yield seen

        return list(get_recursive_type(items))[0]

    # TODO : Right now I'm saving literal subitem, not subitem_type. Maybe this
    # could be removed in the future? I won't do it just yet because the
    # unittests aren't bulletproof. But revisit this later
    #
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
                if subitem_type not in [stored.get_type() for stored in output[item_type]]:
                    output[item_type].append(subitem)

        return output

    def __iter__(self):
        for item in self.items:
            yield item


class MappingContainerType(Type):
    def __init__(self, obj):
        super(MappingContainerType, self).__init__(obj)
        self.keys = []
        self.values = []
        for key, value in grouping.chunkwise_iter(obj.get_children(), 2):
            self.keys.append(key)
            self.values.append(value)

    @staticmethod
    def is_valid(node):
        return isinstance(node, astroid.Dict)

    def as_str(self):
        # A Container (i.e. dict) is processed as two lists would be
        # and then stitched together to make the final result
        #
        keys = ContainerType(self.keys, include_type=False)
        values = ContainerType(self.values, include_type=False)

        # TODO : Possibly use visit.py to get this, instead.
        if isinstance(self.obj, astroid.Dict):
            container_name = 'dict'
        else:
            raise NotImplementedError('Type: "{type_}" is not supported.'.format(type_=self.obj))

        items_text = make_join_text([keys.as_str(), values.as_str()])
        return make_container_label(container_name, items_text)


class ComprehensionContainerType(Type):

    _comprehension_types = {
        astroid.ListComp: list,
    }

    def __init__(self, obj):
        super(ComprehensionContainerType, self).__init__(obj)

    @staticmethod
    def is_valid(node):
        return isinstance(node, astroid.ListComp)

    def as_str(self):
        # Reference:
        #     The first child is the return item in a list-comprehension
        #
        item = list(self.obj.get_children())[0]
        if SpecialType.is_valid(item):
            item_types = SpecialType(item).as_str()
        else:
            _type = get_type(visit.get_value(item))
            item_types = get_type_name(_type)

        container_type = self._comprehension_types[type(self.obj)]
        container_type_name = get_type_name(container_type)

        return make_container_label(container_type_name, item_types)


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
    def _expand_types(obj, include_type=False):
        obj = visit.get_value(obj)

        if ComprehensionContainerType.is_valid(obj):
            return ComprehensionContainerType(obj, include_type=include_type)

        if MappingContainerType.is_valid(obj):
            return MappingContainerType(obj, include_type=include_type)

        if check.is_itertype(obj):
            return ContainerType(obj, include_type=include_type)

        return Type(obj)

    @staticmethod
    def _change_type_to_str(*objs):
        items = []
        for item in [obj.as_str() for obj in objs]:
            if item not in items:
                items.append(item)

        return make_items_text(items)


@six.add_metaclass(abc.ABCMeta)
class MultiTypeBlock(CommonBlock):
    @classmethod
    def draw(cls, info):
        expected_object = info.get(cls._info_key)

        if not expected_object:
            return []

        lines = []
        indent = ''

        # Check if I need this if-statement
        if info.get('lines'):
            lines = [cls.get_starting_line()]
            indent = environment.get_default_indent()

        obj_types = cls._expand_types(expected_object)
        type_info_as_str = cls._change_type_to_str(*obj_types)

        line = cls._make_line(type_info_as_str, indent=indent)
        lines.append(line)

        return lines

    @abc.abstractproperty
    def _info_key():
        return '_some_key'

    @staticmethod
    def _make_line(obj_type, indent):
        return '{indent}{{:{obj_type}!f}}: {{!f}}.'.format(
            indent=indent,
            obj_type=obj_type,
        )


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
    parents = []
    parent = node.parent
    while parent is not None:
        parents.append(parent)
        parent = parent.parent

    return parents


def _process_as_thirdparty_attribute(obj, wrap=False):
    # This third-party attribute may be an object that is either imported or
    # is actually defined (i.e. accessible) in the current module. Find it.
    #
    def get_import_name(obj):
        try:
            return obj.name
        except AttributeError:
            return get_import_name(obj.expr)

    def get_attribute_name(obj):
        try:
            return obj.attrname
        except AttributeError:
            return ''

    def get_local_function_types(module, obj):
        search_name = get_import_name(obj)
        object_line_number = obj.lineno

        # First, try to see if the object is defined in this module
        for function in module.nodes_of_class(astroid.FunctionDef):
            if function.name == search_name:
                full_info = visit.get_info(function)['functions'][function]['returns']
                # TODO : Note to self. This is very bad. I should not be calling
                # MultiTypeBlock here. Pull out these functions
                #
                obj_types = MultiTypeBlock._expand_types(full_info)
                type_info_as_str = MultiTypeBlock._change_type_to_str(*obj_types)
                return type_info_as_str

        return ''

    def get_local_method_types(module, obj):
        for classobj in module.nodes_of_class(astroid.ClassDef):
            # raise ValueError(classobj)
            pass

    def get_import_path_from_ast(module, obj):
        search_name = get_import_name(obj)
        object_line_number = obj.lineno

        for item in module.nodes_of_class((astroid.ImportFrom, astroid.Import)):
            if item.lineno >= object_line_number:
                break

            # If this is "import X"
            if isinstance(item, astroid.Import):
                for name, alias in item.names:
                    if not alias:
                        alias = name

                    if alias == search_name:
                        return name

            # If it was imported using "from X import Y"
            if isinstance(item, astroid.ImportFrom):
                for name, _ in item.names:
                    if name == search_name:
                        return item.modname + '.' + search_name
        return ''

    module = obj.root()

    if environment.allow_type_follow():
        function_signature = get_local_function_types(module, obj)
        if function_signature:
            return function_signature

        method_signature = get_local_method_types(module, obj)
        if method_signature:
            return method_signature

    # If we reached this point, it means that the object we were looking for
    # isn't defined in the same module as the docstring we are building.

    # TODO : In the future, add a way to traverse up the import and then get
    #        ITS docstring. Right now, this code will just return the name
    #        of the import as a "third-party" name, like <textwrap.dedent>
    #        (and not "str", like it should be)
    #
    attribute_name = get_attribute_name(obj)

    import_path = get_import_path_from_ast(module, obj)
    if import_path and hasattr(obj, 'attrname'):
        import_path += '.' + obj.attrname

    if not import_path:
        # If we couldn't gather an import string from the module's imports, then
        # try to get it from the current file, using the AST info we have
        #
        import_path = get_local_attribute_path(obj)

    if wrap:
        return make_third_party_label(import_path)

    return import_path


def _process_as_thirdparty_func(obj):
    try:
        obj = obj.func
    except AttributeError:
        pass

    return _process_as_thirdparty_attribute(obj, wrap=True)


def _process_as_builtin_func(obj):
    # These are functions that we know the Python output to
    try:
        obj = obj.func
    except AttributeError:
        pass

    function_name_to_astroid_type = {
        'bool': bool,
        'dict': dict,
        'float': float,
        'int': int,
        'list': list,
        'set': set,
        'str': str,
        'tuple': tuple,
    }

    try:
        return function_name_to_astroid_type[obj.name]
    except (AttributeError, KeyError):
        return None


def _process_as_known_object(obj):
    # TODO : Possibly make this condition statement better by moving the logic
    #        outside of _process_as_known_object
    #
    # Search literally by string
    if hasattr(obj, 'func'):
        path_obj = obj.func
    else:
        path_obj = obj

    import_path = get_local_attribute_path(path_obj)

    not_found = object()
    default_function = auto_docstring.get_default(import_path, default=not_found)

    if default_function != not_found:
        return default_function(obj)

    # Search by-module and object
    _split = import_path.split('.')
    module_path = '.'.join(_split[:-1])
    obj_name = _split[-1]

    try:
        module = __import__(module_path, fromlist=[obj_name])
    except (ImportError, ValueError):
        # ImportError: If module_path is not importable
        # ValueError: If module_path is empty
        #
        # If module_path has a value but is not importable, it is likely defined
        # in __main__ or the current module
        #
        return

    real_obj = getattr(module, obj_name)
    default_function = auto_docstring.get_default(real_obj, not_found)

    if default_function != not_found:
        return default_function(obj)


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


def make_container_label(container, items_text):
    if items_text:
        return '{container}[{items_text}]'.format(
            container=container, items_text=items_text)

    return container


def make_join_text(items):
    return ', '.join(items)


def make_items_text(items):
    return ' or '.join(items)


def make_third_party_label(text):
    return '<{text}>'.format(text=text)


def get_local_attribute_path(obj):
    if hasattr(obj, 'name'):
        return obj.name

    base = obj.expr
    bases = [obj.attrname]

    while base:
        if hasattr(base, 'attrname'):
            bases.append(base.attrname)

        if hasattr(base, 'name'):
            bases.append(base.name)
            break

        base = base.expr

    return '.'.join(reversed(bases))


def process_types(obj):
    builtin_type = _process_as_builtin_func(obj)
    if builtin_type:
        return get_type_name(builtin_type)

    known = _process_as_known_object(obj)
    if known:
        return known

    if isinstance(obj, astroid.Attribute):
        return _process_as_thirdparty_attribute(obj, wrap=True)
    elif isinstance(obj, astroid.Call):
        return _process_as_thirdparty_func(obj)
