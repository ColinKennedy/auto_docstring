#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Register default values for standard-library objects and functions.'''

# IMPORT STANDARD LIBRARIES
import os

# IMPORT AUTO-DOCSTRING LIBRARIES
import auto_docstring
# TODO : Make this relative
from auto_docstring.blocks.google import common_type


auto_docstring.register('str.format', returns='str')
auto_docstring.register('str.join', returns='str')
auto_docstring.register('textwrap.dedent', returns='str')

def get_getenv_return_types(obj):
    '''Parse os.getenv to get its return types.

    os.getenv can return multiple types.

    os.getenv('foo') returns str or NoneType
    os.getenv('foo', False) returns str or bool.

    Args:
        obj (`astroid.Call`): The os.getenv call to parse.

    Returns:
        str: The return types of this function.

    '''
    all_types = []
    args = obj.args
    for arg in args:
        all_types.append(common_type.process_types(arg))

    if len(args) == 1:
        all_types.append('str')
        all_types.append('NoneType')

    return common_type.make_items_text(all_types)

auto_docstring.register(os.getenv, returns=get_getenv_return_types)
