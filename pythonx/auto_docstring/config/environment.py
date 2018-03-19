#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module for loading and storing user customization settings.'''

# IMPORT STANDARD LIBRARIES
import os
import re


# TODO : Make OPTIONS useful
OPTIONS = {
    'style': os.getenv('AUTO_DOCSTRING_STYLE', 'google'),
}
_STYLES = dict()
_STYLE_BLOCK_ORDER_COMPILE = re.compile(r'(?P<name>\w+):(?P<blocks>[\w+,]):')


def allow_type_follow():
    '''Check if it is OK to follow the type of a Call or Name object.

    Returns:
        bool: If False and a function calls another function, auto_docstring
              will not attempt to get the called function's return type(s).
              If True, it will recursively travel up the called function until
              it has found all its return types. Default is True.

    '''
    try:
        return bool(int(os.getenv('AUTO_DOCSTRING_TYPE_FOLLOW', '1')))
    except TypeError:
        return True


# TODO : Remove this function, later
def get_block_order(name):
    '''Find the order to display docstring blocks.

    If the user has environment variable settings like this:

    environment
    ```
    export AUTO_DOCSTRING_BLOCK_ORDER = "google:args,raises,returns:sphinx:foo:"
    ```

    >>> get_block_order('google')
    >>> # Result: ['args', 'raises', 'returns']

    Args:
        name (str): The name of the style to get block-order of.

    Returns:
        tuple[str]: The order of blocks.

    '''
    order_info = os.getenv('AUTO_DOCSTRING_BLOCK_ORDER', '')

    for style, blocks in _STYLE_BLOCK_ORDER_COMPILE.findall(order_info):
        if style != name:
            continue

        output_blocks = []
        for block in blocks.split(','):
            block = block.strip()
            if block and block not in output_blocks:
                output_blocks.append(block)

        return tuple(output_blocks)

    # Fall-back to the class definition, if no env var for that style was defined
    try:
        style_class = _STYLES[name]
    except KeyError:
        return tuple()

    return style_class.get_default_block_order()


# TODO : Change name to get_indent
def get_default_indent():
    '''The preferred indentation for the auto-generated docstrings.

    Returns:
        str: The indentation. Default: "    ".

    '''
    return os.getenv('AUTO_DOCSTRING_INDENT', '    ')


def get_trailing_characters_to_drop():
    '''Get the character(s) to remove from exception messages.

    ```
    export AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS = "."
    ```

    Example:
        >>> def foo():
        ...     raise ValueError('Some message.')

    Generated docstring:

    Raises:
        ValueError: Some message.

    ```
    export AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS = ""
    ```

    Generated docstring:

    Raises:
        ValueError: Some message..

    Returns:
        str: The characters to remove.

    '''
    return os.getenv('AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS', '.')


# TODO : Add this to __init__.py
def get_all_style_info():
    '''dict[str, object]: The name of a docstring style and its Python object.'''
    return _STYLES


# TODO : Finish this docstring
def register_code_style(name, obj):
    '''Add a new code style to auto_docstring.

    Args:
        name (str): The name of the code-style to use.
        obj: The Python class needed to generate this style's docstrings.

    '''
    _STYLES[name] = obj


def drop_trailing_characters(text, characters=''):
    '''Drop trailing characters from the given text.

    Args:
        text (str):
            The text to strip.
        characters (`str`, optional):
            If given, these characters will be stripped from the end of `text`.
            If nothing is given, `text` is stripped based on the characters
            found in AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS.
            Default: "".

    Returns:
        str: The stripped text.

    '''
    if not characters:
        # TODO : Allow ',' separated list of characters that can be dropped
        characters = get_trailing_characters_to_drop()

    character_length = -1 * len(characters)
    if text[character_length:] == characters:
        return text[:character_length]
    return text
