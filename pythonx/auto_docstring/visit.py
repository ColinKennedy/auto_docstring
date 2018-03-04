#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import importlib
import collections

# IMPORT THIRD-PARTY LIBRARIES
import six
import astroid


class Visitor(object):
    def __init__(self):
        super(Visitor, self).__init__()
        self.functions = collections.defaultdict(dict)

    def visit_functiondef(self, node):
        info = {
            'args': [],
            'defaults': [],
            'in': node.parent,
        }

        number_of_defaults = len(node.args.defaults)
        all_args = list(node.args.get_children())
        defaults = []

        if number_of_defaults:
            args = all_args[:-2 * (number_of_defaults)]
            defaults = all_args[-2 * (number_of_defaults):]
        else:
            args = all_args

        for arg in args:
            info['args'].append(arg.name)

        values = defaults[len(defaults) // 2:]
        defaults = defaults[:len(defaults) // 2:]

        for default, value, in six.moves.zip(defaults, values):
            value = get_object(value)
            info['defaults'].append((default.name, value))

        self.visit(node)

        self.functions[node].update(info)

    def visit(self, node):
        for child in node.get_children():
            try:
                child.accept(self)
            except AttributeError:
                self.visit(child)

    def visit_return(self, node):
        function = node.scope()
        obj = get_object(node.value)
        self.functions[function].setdefault('returns', [])
        self.functions[function]['returns'].append(obj)

    def visit_yield(self, node):
        function = node.scope()
        value = get_value(node.value)
        self.functions[function].setdefault('yields', [])
        self.functions[function]['yields'].append(value)

    # visit_functiondef = visit
    # visit_for = visit
    # visit_if = visit
    # visit_arguments = visit
    # visit_assignname = visit
    # visit_call = visit


def process_function(node):
    visitor = Visitor()
    node.accept(visitor)

    return visitor.functions


def get_info(node):
    output = {'nodes': dict()}
    functions = recursive_default_dict()

    for child in node.get_children():
        if isinstance(child, astroid.FunctionDef):
            for function, info in six.iteritems(process_function(child)):
                functions[function] = info
                output['nodes'][function] = 'functions'

    functions = default_to_regular(functions)
    output['functions'] = functions

    return output


def get_closest_docstring_node(row, info):
    closest_node = None
    closest_row = 0
    functions = info.get('functions', [])
    for function in functions:
        if function.lineno <= row and function.lineno > closest_row:
            closest_node = function
            closest_row = function.lineno

    return closest_node


def get_object(obj):
    if isinstance(obj, (astroid.Call, astroid.Attribute)):
        # TODO : Delete the comment section here, later
        parent = list(obj.infer())[0]
        module = '.'.join([parent_.name for parent_ in _get_parent(parent)])
        module = importlib.import_module(module)
        return getattr(module, parent.name)

    return obj.value


def get_value(node):
    iterable_types = {
        astroid.List: [],
        astroid.Tuple: tuple(),
    }
    try:
        return node.value
    except AttributeError:
        pass

    container = iterable_types[type(node)]
    _temp_container = []
    for item in node.elts:
        _temp_container.append(item)

    return container.__class__(_temp_container)


def recursive_default_dict():
    return collections.defaultdict(recursive_default_dict)


def default_to_regular(d):
    if isinstance(d, collections.defaultdict):
        d = {k: default_to_regular(v) for k, v in six.iteritems(d)}
    return d


def _get_parent(obj):
    def __get_parent(obj):
        try:
            parent = obj.parent
        except AttributeError:
            return
            yield
        else:
            yield parent

        for parent in __get_parent(obj.parent):
            if parent:
                yield parent

    return list(__get_parent(obj))

