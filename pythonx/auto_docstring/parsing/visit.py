#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The module that is responsible for parsing Python source-code.

The source-code is parsed to find information needed to build docstrings.

'''

# IMPORT STANDARD LIBRARIES
import collections

# IMPORT THIRD-PARTY LIBRARIES
import six
import astroid


class Visitor(object):

    '''A class that recursively walks AST Nodes and gathers docstings data.'''

    def __init__(self):
        '''Create an object to store informatino about functions.'''
        super(Visitor, self).__init__()
        self.functions = collections.defaultdict(dict)

    def visit_functiondef(self, node):
        '''Get the given FunctionDef `node` args.

        Args:
            node (<astroid.FunctionDef>): The node to get info for.

        '''
        info = {
            'args': [],
            'defaults': [],
            'in': node.parent,
        }

        all_args = self._get_all_args(node)
        args, defaults = self._organize_args(node, all_args)

        for arg in args:
            info['args'].append(arg.name)

        for default, value, in six.moves.zip(*defaults):
            info['defaults'].append((default.name, value))

        info['vararg'] = node.args.vararg
        info['kwarg'] = node.args.kwarg

        self.functions[node].update(info)

        # Recurse through the node's children so we can find more nodes
        self.visit(node)

    def visit(self, node):
        '''Visit the given Node's children.'''
        for child in node.get_children():
            try:
                child.accept(self)
            except AttributeError:
                self.visit(child)

    def visit_raise(self, node):
        '''Add raise statements to this instance's function information.'''
        function = node.scope()
        self.functions[function].setdefault('raises', [])
        self.functions[function]['raises'].append(node)

    def visit_return(self, node):
        '''Whenever a Return object is found, get its parent scope and store it.

        Args:
            node (<astroid.Return>): The node to get info for.

        '''
        def is_yield_return(node):
            '''If `node` is a return/yield statement.

            Args:
                node (:class:`astroid.Return`): The node to check.

            Example:
                >>> def foo():
                ...     return
                ...     yield

            '''
            sibling = node.next_sibling()
            node_column_offset = node.col_offset

            while sibling is not None:
                is_in_same_statement = node_column_offset == sibling.col_offset
                if isinstance(sibling.value, astroid.Yield) and is_in_same_statement:
                    return True

                if not is_in_same_statement:
                    return False

                sibling = sibling.next_sibling()

            return False

        if is_yield_return(node):
            return

        function = node.scope()
        self.functions[function].setdefault('returns', [])
        self.functions[function]['returns'].append(node.value)

    def visit_yield(self, node):
        '''Whenever a Yield object is found, get its parent scope and store it.

        Args:
            node (<astroid.Return>): The node to get info for.

        '''
        def is_blank_yield(node):
            '''If `node` is a return/yield statement.

            Args:
                node (:class:`astroid.Yield`): The node to check.

            Example:
                >>> def foo():
                ...     return
                ...     yield

            '''
            sibling = node.previous_sibling()
            node_column_offset = node.col_offset

            while sibling is not None:
                is_in_same_statement = node_column_offset == sibling.col_offset
                if isinstance(sibling, astroid.Return) and is_in_same_statement:
                    return True

                sibling = sibling.previous_sibling()

            return False

        if is_blank_yield(node):
            return

        function = node.scope()

        self.functions[function].setdefault('yields', [])
        self.functions[function]['yields'].append(node.value)

    @staticmethod
    def _get_all_args(node):
        '''Find the args for the given `node`.

        If the node is a classmethod or instancemethod, drop the first arg.

        Args:
            node (<astroid.FunctionDef>): The node to get the args of.

        Returns:
            list[<astroid Node>]:
                The full list of args. This list contains positional args
                that do and do not have default values.

        '''
        try:
            decorators = node.decorators.get_children()
        except AttributeError:
            decorators = []

        children = list(node.args.get_children())

        drop_first_arg = isinstance(node.parent, astroid.ClassDef)

        if not drop_first_arg:
            return children

        for decorator in decorators:
            if decorator.name == 'staticmethod':
                return children

        return children[1:]

    @staticmethod
    def _organize_args(node, args):
        '''Sort the given `args` and return them as two separate lists.

        Basically, FunctionDef.get_children() is overly complicated. It returns
        back the positional args of the function and its default values
        in a single list.

        Example:
            >>> def foo(bar, fizz=8, buzz=123.3):
            >>>     pass

            >>> <FunctionDef.foo>.get_children()
            ... # [AssignName.bar, AssignName.fizz, AssignName.buzz, Const.int, Const.float]

        So we have to split up this list from
            >>> [AssignName.bar, AssignName.fizz, AssignName.buzz, Const.int, Const.float]

        to
            >>> ([AssignName.bar], ([AssignName.fizz, AssignName.buzz], [Const.float, Const.int])

        Args:
            args (list[<astroid Node>]): The args to organize.

        Returns:
            tuple[
                list[<astroid.AssignName>],
                tuple[list[<astroid.AssignName>], list[<astroid Node>]]:
                    The positional, required args, followed by args that
                    have default values and then the list of default values.

        '''
        number_of_defaults = len(node.args.defaults)

        defaults = []
        if number_of_defaults:
            defaults = args[-2 * (number_of_defaults):]
            args = args[:-2 * (number_of_defaults)]

        values = defaults[len(defaults) // 2:]
        defaults = defaults[:len(defaults) // 2:]

        return (args, (defaults, values))


def get_info(node):
    '''Get everything needed to build docstrings from the given `node`.

    Args:
        node (<astroid.Module>): The node to break down into parts.

    Returns:
        dict[str]: The
            "functions" (dict[<astroid.FunctionDef>, dict[str]]):
                A function node and all of its gathered information.
            "nodes" (dict[<astroid Node>, str]):
                The found node and what group it belongs to. This string
                should be a different key in this dictionary.
                Example: "functions".

    '''
    output = {'nodes': dict()}

    visitor = Visitor()
    try:
        node.accept(visitor)
    except AttributeError:
        visitor.visit(node)

    functions = visitor.functions
    for function, info in six.iteritems(functions):
        functions[function] = info
        output['nodes'][function] = 'functions'

    functions = default_to_regular(functions)
    output['functions'] = functions

    return output


def get_closest_docstring_node(row, info):
    '''Find the FunctionDef node whose docstring is closest to the given `row`.

    Args:
        row (int): The point in the code to use to find a FunctionDef node.
        info (dict[str]): The known Node objects that will be used.

    Returns:
        <astroid Node>: The found astroid.FunctionDef node.

    '''
    closest_node = None
    closest_row = 0
    functions = info.get('functions', [])
    for function in functions:
        if function.lineno <= row and function.lineno > closest_row:
            closest_node = function
            closest_row = function.lineno

    return closest_node


def get_container_types():
    '''dict[type, type]: Convert an iterable type with a Python iterable type.'''
    return \
        {
            list: list,
            tuple: tuple,
            astroid.List: list,
            astroid.Tuple: tuple,
        }


def get_container(node):
    '''Create an iterable object from the given `node`.'''
    iterable_types = get_container_types()
    # Build an instance of the container for the given node
    return iterable_types[type(node)]()


def get_value_binop(node):
    '''Get the value of a binary operator.

    Binary operators take on a few forms in Python but the most common is for
    old-style strings, like "%s" % ('foo', ). That would be an example of
    a binary operator using a str and tuple.

    Another example is the "+" sign.

    Returns:
        The found value or NoneType.

    '''
    # TODO : Remove this if-condition
    if not isinstance(node, astroid.BinOp):
        return

    for item in node.get_children():
        value = get_value(item)
        if value:
            return value


def get_type(node):
    '''Convert the given statement `node` to a Python type.

    For example, :class:`astroid.Compare` will always be bool, and
    :class:`astroid.Dict` will always be dict.

    Raises:
        ValueError: If the given node has no valid type.

    Returns:
        The found type.

    '''
    all_types = {
        astroid.Compare: bool,
        astroid.BoolOp: bool,
        astroid.Dict: dict,
    }

    try:
        return all_types[type(node)]
    except KeyError:
        raise ValueError('Node: "{node}" was invalid. Options were: "{all_types}".'
                         ''.format(node=node, all_types=all_types))


def get_value(node):
    '''Get the Python object(s) for the given node.

    If the node is something like a Str or Num, get its value.
    If the node is actually an iterable object that contains other nodes,
    create a Python instance of the container and add its child nodes.

    Args:
        node (<astroid Node>): The node to get the parents of.

    Returns:
        object or iter[<astroid Node>]:
            An instance of the container, with the given `node`'s children.
            If the given `node` is not iterable, return its value.

    '''
    try:
        # Try to see if the node is actually not a container-type
        return node.value
    except AttributeError:
        pass

    value = get_value_binop(node)
    if value:
        return value

    container = get_container(node)

    _temp_container = []
    for item in iterate(node):
        _temp_container.append(item)

    return container.__class__(_temp_container)


def iterate(obj):
    '''Iterate over the given object's items.

    Args:
        obj (iter or <astroid.NodeNG>): The object to iterate.

    Returns:
        iter or generator: The iterable object.

    '''
    try:
        return obj.get_children()
    except AttributeError:
        return obj


def recursive_default_dict():
    '''<collections.defaultdict>: A dict that allows nested mappings.'''
    return collections.defaultdict(recursive_default_dict)


def default_to_regular(obj):
    '''Convert a nested defaultdict into a regular dict.'''
    if isinstance(obj, collections.defaultdict):
        obj = {key: default_to_regular(value) for key, value in six.iteritems(obj)}
    return obj
