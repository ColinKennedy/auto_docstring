#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A collection of classes and functions used to get Python return-types.'''

# IMPORT STANDARD LIBRARIES
import __builtin__
import collections
import importlib
import inspect

# IMPORT THIRD-PARTY LIBRARIES
import astroid
import six

# IMPORT AUTO-DOCSTING LIBRARIES
import auto_docstring

# IMPORT LOCAL LIBRARIES
from ...parsing import assign_search
from ...config import environment
from ...parsing import visit
from ...core import grouping
from ...core import check


class Type(object):

    '''A generic object that is meant to print a Type of Python object.'''

    def __init__(self, obj):
        '''Store the given object.

        Args:
            obj (str or `astroid.NodeNG`):
                The object to store. Can be anything. Usually though, it's
                either some kind of AST node or a string.

        '''
        super(Type, self).__init__()
        self.obj = obj

    def type_contained_in(self, seq):
        '''If this object's type is inside of the given sequence-type.

        Args:
            seq (:class:`auto_docstring.blocks.google.common_block.IterableType`):
                The sequence to check for this object.

        Returns:
            bool: If this object is in the given `seq`.

        '''
        return self.get_type() in [item.get_type() for item in seq]

    def get_type(self):
        '''type: Get the class of the stored object on this instance.'''
        return get_type(self.obj)

    def __eq__(self, other):
        '''bool: If an item has the same stored object as this instance.'''
        try:
            return other.obj == self.obj
        except AttributeError:
            return False

    def as_str(self):
        '''str: Get the string representation of the stored object.'''
        return get_type_name(self.obj)

    def __repr__(self):
        '''str: Show the input needed to re-create this class.'''
        return '{cls_}({obj!r})'.format(
            cls_=self.__class__.__name__,
            obj=self.obj,
        )


class SpecialType(Type):

    '''A Type that contains a node that needs to be "resolved" or "found".

    For example, an `astroid.Call` object may be referring to another function
    in the same module. We use this class to infer the types that the other
    function returns and then use that as its return type(s).

    This class works with `astroid.Call`, `astroid.Name` and `astroid.Attribute`
    objects.

    '''

    def __init__(self, obj):
        '''Create the object and do nothing else.'''
        super(SpecialType, self).__init__(obj)

    @staticmethod
    def is_valid(node):
        '''If the given `node` is able to be parsed by this class.'''
        return isinstance(node, (astroid.Call, astroid.Attribute, astroid.Name))

    # TODO : Check if info is necessary. If not, remove it
    def as_str(self, info=None):
        '''Create a string-representation for this instance.

        The checks for this method are as follows:
            - Check if the object is actually a built-in, callable object.
            - If it isn't built-in but it is callable, get the callable's type
            - If the object is an attribute of another object, try to get its
              actual, fully-resolved path and use to get its type
                - If we could not get the type signature of the callable object
                  or the attribute then just return the name of the object as a
                  "third-party" object. By default, this means "add <>s around
                  the name of the object".
            - If the object is local to the module that `self.obj` is part of,
              try to get its signature
            - If we cannot get the signature of the local object then, we will
              try to rely on astroid to "infer" the object's type.
                  - If that fails, it may be because astroid could not infer the
                    type of the object because the object was assigned earlier
                    in the module. In which case, try to get the `astroid.Assign`
                    by "searching" for wherever this object was defined
                    in the module. This has a pretty small chance of happening.

        The entire check-process is recursive. If a check encounters another
        Attribute, Name, Call, or Foo object that it doesn't understand, it will
        keep digging until it can find a type.

        Returns:
            str: The created type string.

        '''
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
        return self.get_import_path(obj)

    @staticmethod
    def get_import_path(obj):
        '''Find the full '.' import path for the given object.

        Args:
            obj (type): Some built-in Python type, like list, tuple, etc.

        Returns:
            str: The name of the given `obj`.

        '''
        def is_builtin_type(obj):
            '''bool: If the given object is a built-in Python object.'''
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

        raise NotImplementedError('Need to write the rest of this')
        # name = obj.__name__
        # parent = inspect.getmodule(obj).__name__

        # return make_third_party_label('{parent}.{name}'.format(parent=parent, name=name))

    @staticmethod
    def search(obj):
        '''Find the type of the given `obj` by searching for where it was assigned.

        Args:
            obj (`astroid.Name`): Some variable whose type will be retrieved.

        Returns:
            str: The name of the found type.

        '''
        outer_scope = obj.scope()
        try:
            found_type = assign_search.find_node_type(outer_scope, name=obj.name)
        except RuntimeError:
            raise ValueError('Obj: "{obj}" was not assigned.'.format(obj=obj))

        return get_type_name(found_type)


class IterableType(Type):

    '''A type of Type that contains other Types.

    Normally, this object is used to parse iterable objects, like list or tuple.
    However, it can be generally useful to other class objects, too.
    See :class:`auto_docstring.blocks.google.common_block.ContainerType`
    for details.

    '''

    def __init__(self, node, include_type=True):
        '''Create the object and cast `obj`'s subitems into Type objects.

        Args:
            node (`astroid.NodeNG`):
                Some iterable node to break into pieces, recursively.
            include_type (`bool`, optional):
                If True then the type of `node` will be included in the
                string representation of this object, any time as_str is called.
                If False, then this instance will only print its subitem's types
                and `node` type will be ignored. Default is True.

        '''
        super(IterableType, self).__init__(node)
        self.items = []
        self.include_type = include_type

        for subitem in visit.iterate(node):
            # If it's a Name or Call object and its type needs to be inferred
            # TODO : Replace with classmethods
            if SpecialType.is_valid(subitem):
                self.items.append(SpecialType(subitem))
                continue

            # If it's a pairwise container, like a dict
            if ContainerType.is_valid(subitem):
                self.items.append(ContainerType(subitem))
                continue

            if DictComprehensionContainerType.is_valid(subitem):
                self.items.append(DictComprehensionContainerType(subitem))
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
            try:
                value = visit.get_value(subitem)
            except KeyError:
                # This happens if no value could be found. If that's the case
                # then just ignore it. It's probably a scenario whose type
                # cannot be easily inferred.
                #
                # Example: "a + b" is not easily inferred because a could be
                # an instance of a class that overrides __add__
                # to something totally arbitrary.
                #
                pass
            else:
                self.items.append(Type(value))

    def type_contained_in(self, seq):
        '''If this each of the types is contained in the given sequence-type.

        Args:
            seq (:class:`auto_docstring.blocks.google.common_block.IterableType`):
                The sequence to check for this object and its subitems.

        Returns:
            bool: If this object is in the given `seq`.

        '''
        result = super(IterableType, self).type_contained_in(seq)
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
        '''str: Create a string-representation for this instance.'''
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

    # TODO : Rename this method. Obviously it is not named well
    # TODO : Is it possible to use short-hand?
    def _reduce(self, items):
        '''Remove redundant subitems in `items` so only unique types remain.

        Note:
            This method preserves type order.

        Returns:
            list[:class:`auto_docstring.blocks.google.common_block.Type`]: The unique objects.

        '''
        def get_recursive_type(obj):
            '''Recursively get all of the types of the given `obj`.

            Warning:
                Changes to this function are discouraged.
                Be careful of cyclic loops.

            Yields:
                Type: The found subitems of `obj`.

            '''
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

    # TODO : Provide example input/output in the docstring
    def _group(self, items):
        '''Collect the unique types of each of the given items into a dict.

        Other methods are responsible for either getting types of objects or
        filtering their types. This method is responsible for making sure
        that each container-type only lists its child types once.

        Args:
            items (iter[:class:`auto_docstring.blocks.google.common_block.Type`]):
                The items to group.

        Returns:
            `collections.OrderedDict`: The grouped items.

        '''
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
        '''Type: Get every sub-item in this instance.'''
        for item in self.items:
            yield item


class ContainerType(Type):

    '''A special type, specifically for hash-table Types, like dict.

    This class works by treating keys and values as if they are two
    IterableType objects and storing both, at the same time.

    It's very incorrect to assume that a dict is actually just two lists
    but, since we only are concerned with displaying the types of keys
    and values once, it actually turned out to be a great way to re-use code.

    '''

    def __init__(self, obj):
        '''Create the object and store two Containers, for the keys and values.

        Args:
            obj (`astroid.Dict`): The mapping object to split into types.

        '''
        super(ContainerType, self).__init__(obj)
        self.keys = []
        self.values = []
        for key, value in grouping.chunkwise_iter(obj.get_children(), 2):
            self.keys.append(key)
            self.values.append(value)

    @staticmethod
    def is_valid(node):
        '''bool: Check if the given node is a dict or mapping object.'''
        return isinstance(node, astroid.Dict)

    def as_str(self):
        '''str: Create a string-representation for this instance.

        Raises:
            NotImplementedError: If the stored type on this instance is invalid.

        Returns:
            str: The string-representation of this instance.

        '''
        # A Container (i.e. dict) is processed as two lists and
        # then stitched together to make the final result
        #
        keys = IterableType(self.keys, include_type=False)
        values = IterableType(self.values, include_type=False)

        # TODO : Possibly use visit.py to get this, instead.
        if isinstance(self.obj, astroid.Dict):
            container_name = 'dict'
        else:
            raise NotImplementedError('Type: "{type_}" is not supported.'.format(type_=self.obj))

        items_text = make_join_text([keys.as_str(), values.as_str()])
        return make_container_label(container_name, items_text)


class ComprehensionContainerType(Type):

    '''A Type class which is used to express a Python list-comprehension.'''

    _comprehension_types = {
        astroid.ListComp: list,
    }

    def __init__(self, obj):
        '''Create this object and store the given `obj`.

        Args:
            obj (`astroid.ListComp`): The node to store.

        '''
        super(ComprehensionContainerType, self).__init__(obj)

    @staticmethod
    def is_valid(node):
        '''Check if the given node can be processed by this class.

        Args:
            node (`astroid.ListComp`): The node to check.

        Returns:
            bool: If the node is some kind of list-comprehension object.

        '''
        return isinstance(node, astroid.ListComp)

    def as_str(self):
        '''str: Get the stored list-comprehension node as a type-docstring.'''
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


class DictComprehensionContainerType(Type):
    def __init__(self, obj):
        super(DictComprehensionContainerType, self).__init__(obj)

    @staticmethod
    def is_valid(node):
        return isinstance(node, astroid.DictComp)

    def as_str(self):
        return 'dict'


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


# TODO : Move this inner functions out
def _process_as_thirdparty_attribute(node, wrap=False):
    '''Get the string representation of some `node`.

    Args:
        node (`astroid.Attribute`):
            The node to get the type's name of.
        wrap (`bool`, optional):
            If True, a "third-party label" (by default, <>s) will be added
            to the result of this function. If False, no <>s will be added.
            Default is False.

    Returns:
        str: The found type for the given `node`.

    '''
    # TODO : This function is messed up. Double-Check it
    def get_end_name_of_node(obj):
        '''Get the tail-name of the given `obj`.

        Args:
            obj (`astroid.Name` or `astroid.Attribute`):
                The node to get the name of.

        Returns:
            str: The found name for the given `obj`.

        '''
        try:
            return obj.name
        except AttributeError:
            try:
                # If the attribute path contains an `astroid.Call` object then
                # we need to get the `func`. Otherwise, `expr` will fail
                #
                obj = obj.func
            except AttributeError:
                pass

            return get_end_name_of_node(obj.expr)

    # TODO : Couldn't I just if function == obj?
    def get_local_function_types(module, node):
        '''Look at the given `module` defined functions and try to find `node`.

        Args:
            module (`astroid.Module`): The module that defines `node`.
            node (`astroid.Name` or `astroid.Attribute`):
                The node to try to find the function definition for.

        Returns:
            str: The found types for the local function that defines `node`.
                 If no function types were found, return an empty string.

        '''
        from . import common_block
        search_name = get_end_name_of_node(node)

        # First, try to see if the object is defined in this module
        for function in module.nodes_of_class(astroid.FunctionDef):
            if function.name == search_name:
                full_info = visit.get_info(function)['functions'][function]['returns']
                # TODO : Note to self. This is very bad. I should not be calling
                # MultiTypeBlock here. Pull out these functions
                #
                obj_types = common_block.MultiTypeBlock._expand_types(full_info)
                type_info_as_str = common_block.MultiTypeBlock._change_type_to_str(*obj_types)
                return type_info_as_str

        return ''

    # def get_local_method_types(module, obj):
    #     # for classobj in module.nodes_of_class(astroid.ClassDef):
    #     #     # raise ValueError(classobj)
    #     #     pass

    # TODO : Maybe move "wrap" out of this parameter and just add it to parent
    #        functions wherever it is used
    #
    def get_import_path_from_ast(module, node, wrap=False):
        '''Find the dot "." import path, using the given `obj` AST node.

        Args:
            module (`astroid.Module`):
                The module that defines `node`.
            node (`astroid.Name` or `astroid.Attribute`):
                The node to try to find the function definition for.
            wrap (`bool`, optional):
                If True, a "third-party label" (by default, <>s) will be added
                to the result of this function. If False, no <>s will be added.
                Default is False.

        Returns:
            str: The path somewhere on the user's PYTHONPATH that could be used
                 to import `node`.

        '''
        search_name = get_end_name_of_node(node)
        object_line_number = node.lineno

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

    # This third-party attribute may be an object that is either imported or
    # is actually defined (i.e. accessible) in the current module. Find it.
    #
    module = node.root()

    if environment.allow_type_follow():
        function_signature = get_local_function_types(module, node)
        if function_signature:
            return function_signature

        # TODO : Finish this
        # method_signature = get_local_method_types(module, node)
        # if method_signature:
        #     return method_signature

    # If we reached this point, it means that the object we were looking for
    # isn't defined in the same module as the docstring we are building.

    # TODO : In the future, add a way to traverse up the import and then get
    #        ITS docstring. Right now, this code will just return the name
    #        of the import as a "third-party" name, like <textwrap.dedent>
    #        (and not "str", like it should be)
    #
    import_path = get_import_path_from_ast(module, node, wrap=wrap)
    if import_path and hasattr(node, 'attrname'):
        import_path += '.' + node.attrname

    if not import_path:
        # If we couldn't gather an import string from the module's imports, then
        # try to get it from the current file, using the AST info we have
        #
        import_path = get_local_attribute_path(node)

    if wrap:
        return make_third_party_label(import_path)

    return import_path


def _process_as_thirdparty_func(obj):
    '''Find the return type(s) from a callable object.

    Args:
        obj (`astroid.NodeNG`): The callable object to parse.

    Returns:
        str: The type(s) of the callable object.

    '''
    try:
        obj = obj.func
    except AttributeError:
        pass

    return _process_as_thirdparty_attribute(obj, wrap=True)


def _process_as_builtin_func(obj):
    '''Get the type of a builtin attribute or callable function.

    This function assumes that `obj` is an `astroid.Name` or `astroid.Call`
    node which represents a built-in Python type.

    Args:
        obj (`astroid.NodeNG`): The node which represents a built-in type.

    Returns:
        str: The string representation of the given node's Python type.

    '''
    # These are functions that we know the Python output to
    try:
        obj = obj.func
    except AttributeError:
        pass

    function_name_to_astroid_type = {
        'all': bool,
        'any': bool,
        'bool': bool,
        'callable': bool,
        'dict': dict,
        'float': float,
        'hasattr': bool,
        'int': int,
        'isinstance': bool,
        'issubclass': bool,
        'len': int,
        'list': list,
        'repr': str,
        'round': int,
        'set': set,
        'sorted': list,
        'str': str,
        'tuple': tuple,
        'type': type,
        'unicode': unicode,
    }

    try:
        return function_name_to_astroid_type[obj.name]
    except (AttributeError, KeyError):
        return None


# TODO : Check that this docstring is actually correct
def _process_as_known_object(obj):
    '''Get the type of an object that the user has pre-defined type(s) of.

    Example:
        >>> auto_docstring.register('some_name', returns='foo')
        >>> def foo():
        ...     return some_name

        Will generate the docstring, """{1:foo!f}: {2!f}."""

    Args:
        obj (`astroid.NodeNG`): The node to parse.

    Returns:
        str or NoneType: The found type-name for the node,
                         if the node was pre-registered.

    '''
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


def get_type(obj):
    '''type: Get the class object for the given `obj`.'''
    return obj.__class__


def get_type_name(obj):
    '''str: Get the name of the class of the given `obj`.'''
    if not inspect.isclass(obj):
        obj = get_type(obj)

    return obj.__name__


def get_local_attribute_path(node):
    '''Infer the attribute dot (".") of the given `node`.

    Args:
        node (`astroid.Attribute`): The node to get a dot string of.

    Returns:
        str: The found dot string.

    '''
    if hasattr(node, 'name'):
        return node.name

    base = node.expr
    bases = [node.attrname]

    # Get the whole path, going from right to left
    while base:
        try:
            # If the attribute path contains an `astroid.Call` object then
            # we need to get the `func`. Otherwise, `expr` will fail
            #
            base = base.func
        except AttributeError:
            pass

        if hasattr(base, 'attrname'):
            bases.append(base.attrname)

        if hasattr(base, 'name'):
            bases.append(base.name)
            break

        base = base.expr

    # We retrieved the attribute path backwards since we went right to left
    # so reverse it and return it
    #
    return '.'.join(reversed(bases))


# TODO : Possibly change this to just return "" if nothing is found. Check unittests
def process_types(node):
    '''Get the type of the given `node` as a string.

    This function checks if `node` is a built-in Python object, then it will
    check if the user registered an explicit value for it.

    If it can't find either, it will try to find the type of `node` by searching
    through other functions and methods recursively in the same file. If the
    object is imported, it will import the module that `node` is contained
    within recursively until a type is found.

    Args:
        node (`astroid.Node`): The node to convert to a string.

    Returns:
        str or NoneType: The found type, if any.

    '''
    builtin_type = _process_as_builtin_func(node)
    if builtin_type:
        return get_type_name(builtin_type)

    known = _process_as_known_object(node)
    if known:
        return known

    if isinstance(node, astroid.Attribute):
        return _process_as_thirdparty_attribute(node, wrap=True)
    elif isinstance(node, astroid.Call):
        return _process_as_thirdparty_func(node)


def make_container_label(container, items_text=''):
    '''Get a string representation of the given container, assuming it has items.

    Example:
        >>> make_container_label(container='list', items_text='str')
        # Result: "list[str]" #

    Args:
        container (str): The name of the container to use.
        items_text (`str`, optional):
            The items that make up the given container. If nothing is given,
            just the name of the container will returned, instead.

    Returns:
        str: The string representation of the given `container` and `items_text`.

    '''
    prefix = environment.get_container_prefix()
    suffix = environment.get_container_suffix()

    if items_text:
        return '{container}{prefix}{items_text}{suffix}'.format(
            container=container,
            prefix=prefix,
            items_text=items_text,
            suffix=suffix
        )

    return container


# TODO : Make this configure-able
def make_join_text(items):
    '''str: Combine the given `items` with the user's prefered join-text.'''
    return ', '.join(items)


# TODO : Make this configure-able
def make_items_text(items):
    '''str: Combine the given `items` with the user's prefered choice-text.'''
    join_text = environment.get_option_separator()
    return join_text.join(items)


# TODO : Make this configure-able
def make_third_party_label(text):
    '''str: Wrap `text` in a label that means "this is a third-party object".'''
    return '<{text}>'.format(text=text)
