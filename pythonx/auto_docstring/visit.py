#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import importlib
import collections

# IMPORT THIRD-PARTY LIBRARIES
import six
import astroid


def process_function(node):
    # Parse the args/kwargs of the function
    info = {
        'args': [],
        'defaults': [],
        'in': node.parent,
        'returns': [],
    }

    number_of_defaults = len(node.args.defaults)
    all_args = list(node.args.get_children())

    if number_of_defaults:
        args = all_args[:-2 * (number_of_defaults)]
    else:
        args = all_args

    defaults = all_args[-2 * (number_of_defaults):]

    for arg in args:
        info['args'].append(arg.name)

    values = defaults[len(defaults) // 2:]
    defaults = defaults[:len(defaults) // 2:]

    for default, value, in six.moves.zip(defaults, values):
        value = get_object(value)
        info['defaults'].append((default.name, value))

    # Gather return-data
    for item in node.body:
        if isinstance(item, astroid.Return):
            value = item.value.value
            info['returns'].append(value)

    return info


def get_info(node):
    output = {'nodes': dict()}
    functions = recursive_default_dict()

    for child in node.get_children():
        if isinstance(child, astroid.FunctionDef):
            functions[child] = process_function(child)
            output['nodes'][child] = 'functions'

    functions = default_to_regular(functions)
    output['functions'] = functions

    return output


def get_closest_docstring_node(row, info):
    closest_node = None
    closest_row = 0
    functions = info.get('functions', [])
    for function in functions:
        if function.lineno <= row:
            closest_node = function
            closest_row = function.lineno

    return closest_node


def get_object(obj):
    def get_parent(obj):
        def _get_parent(obj):
            try:
                parent = obj.parent
            except AttributeError:
                return
                yield
            else:
                yield parent

            for parent in _get_parent(obj.parent):
                if parent:
                    yield parent

        return list(_get_parent(obj))

    if isinstance(obj, astroid.Call):
        # TODO : Delete the comment section here, later
        parent = list(obj.infer())[0]
        module = '.'.join([parent_.name for parent_ in get_parent(parent)])
        module = importlib.import_module(module)
        return getattr(module, parent.name)

        # parent = list(obj.infer())[0]
        # import_path = '.'.join([parent_.name for parent_ in get_parent(parent)] + [parent.name])
        # return '<{}>'.format(import_path)

    return obj


def recursive_default_dict():
    return collections.defaultdict(recursive_default_dict)


def default_to_regular(d):
    if isinstance(d, collections.defaultdict):
        d = {k: default_to_regular(v) for k, v in six.iteritems(d)}
    return d
