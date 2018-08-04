#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Register default values for standard-library objects and functions.'''

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from ...auto_docstring.blocks.google import common_type
from .. import registry


def get_getenv_return_types(obj):
    '''Parse os.getenv to get its return types.

    Note:
        os.getenv can potentially return multiple types.
        os.getenv('foo') returns str or NoneType
        os.getenv('foo', False) returns str or bool.

    Args:
        obj (`astroid.Call`): The os.getenv call to parse.

    Returns:
        str: The return types of this function.

    '''
    all_types = ['str']
    try:
        arg = obj.args[1]
    except IndexError:
        all_types.append('NoneType')
    else:
        all_types.append(common_type.process_types(arg) or 'NoneType')

    return common_type.make_items_text(all_types)


registry.register(os.getenv, returns=get_getenv_return_types)
registry.register('str.format', returns='str')
registry.register('str.join', returns='str')
registry.register('textwrap.dedent', returns='str')
