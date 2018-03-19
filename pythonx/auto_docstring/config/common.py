#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of very generic functions used by auto_docstring.'''

# IMPORT STANDARD LIBRARIES
import uuid

# IMPORT LOCAL LIBRARIES
from . import environment


def get_code_style(name):
    '''Get the Python object needed to generate docstrings for the given style.

    Args:
        name (str): The name of the style to get.

    Raises:
        ValueError: If the given name was not a registered code-style.

    Returns:
        The object registered for this code-style. For all styles and objects,
        check out :func:`auto_docstring.get_all_style_info`.

    '''
    styles = environment.get_all_style_info()
    try:
        return styles[name]
    except KeyError:
        raise ValueError('Style: "{name}" was invalid. Options were, "{options}".'
                         ''.format(name=name, options=sorted(styles.keys())))


def get_unique_number():
    '''int: Get a unique (non-repeated) number value.'''
    return uuid.uuid4().int


def create_code_style(name):
    '''Get the Python object needed to generate docstrings for the given style.

    Args:
        name (str): The name of the style to get.

    Returns:
        The object registered for this code-style. For all styles and objects,
        check out :func:`auto_docstring.get_all_style_info`.

    '''
    style = get_code_style(name)
    return style
