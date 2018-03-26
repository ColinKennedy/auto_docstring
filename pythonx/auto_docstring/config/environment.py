#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module for loading and storing user customization settings.'''

# IMPORT STANDARD LIBRARIES
import collections
import os
import re


_STYLES = dict()
_STYLE_BLOCK_ORDER_COMPILE = re.compile(r'(?P<name>\w+):(?P<blocks>[\w,]+):')
_CONFIG = collections.defaultdict(list)


def register_config_entry(name, predicate):
    _CONFIG[name].insert(0, predicate)


def get_config_entry(name, default=None):
    for function in _CONFIG[name]:
        try:
            return function()
        except Exception:
            pass

    return default


def _auto_raw_prefix():
    return os.environ['AUTO_DOCSTRING_RAW_PREFIX'] == '1'


def auto_raw_prefix():
    return get_config_entry('raw_prefix', default=True)


def _allow_type_follow():
    '''Check if it is OK to follow the type of a Call or Name object.

    Returns:
        bool: If False and a function calls another function, auto_docstring
              will not attempt to get the called function's return type(s).
              If True, it will recursively travel up the called function until
              it has found all its return types. Default is True.

    '''
    return os.environ['AUTO_DOCSTRING_TYPE_FOLLOW'] == '1'


def allow_type_follow():
    return get_config_entry('type_follow', default=True)


# TODO : Add this to __init__.py
def get_all_style_info():
    '''dict[str, object]: The name of a docstring style and its Python object.'''
    return _STYLES


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
    def get_default_style_blocks(name):
        try:
            style_class = _STYLES[name]
        except KeyError:
            return tuple()

        return style_class.get_default_block_order()

    order_info = os.getenv('AUTO_DOCSTRING_BLOCK_ORDER', '')

    if not order_info:
        # Fall-back to the class definition, if no env var for that style was defined
        return get_default_style_blocks(name)

    info = _STYLE_BLOCK_ORDER_COMPILE.findall(order_info)

    if not info:
        blocks = []
        for block in order_info.split(','):
            block = block.strip()
            if block and block not in blocks:
                blocks.append(block)

        return tuple(blocks)

    for style, blocks in info:
        if style != name:
            continue

        output_blocks = []
        for block in blocks.split(','):
            block = block.strip()
            if block and block not in output_blocks:
                output_blocks.append(block)

        return tuple(output_blocks)

    return get_default_style_blocks(name)


def _get_container_prefix():
    return os.environ['AUTO_DOCSTRING_CONTAINER_PREFIX']


def get_container_prefix():
    return get_config_entry('container_prefix', default='[')


def _get_container_suffix():
    return os.environ['AUTO_DOCSTRING_CONTAINER_SUFFIX']


def get_container_suffix():
    return get_config_entry('container_suffix', default=']')


# TODO : Change name to get_indent
def _get_default_indent():
    '''The preferred indentation for the auto-generated docstrings.

    Returns:
        str: The indentation. Default: "    ".

    '''
    return os.environ['AUTO_DOCSTRING_INDENT']


def get_default_indent():
    return get_config_entry('indent', default='    ')


def _get_docstring_delimiter():
    return os.environ['AUTO_DOCSTRING_DELIMITER']


def get_docstring_delimiter():
    return get_config_entry('delimiter', default='"""')


def _get_trailing_characters_to_drop():
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
    return os.environ['AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS']


def get_trailing_characters_to_drop():
    return get_config_entry('trailing_characters', default='.')


def _get_current_style():
    return os.environ['AUTO_DOCSTRING_STYLE']


def get_current_style():
    return get_config_entry('style', default='google')


def _get_description_separator():
    return os.environ['AUTO_DOCSTRING_DESCRIPTION_SEPARATOR']


def get_description_separator():
    return get_config_entry('description_separator', default=' ')


def _get_option_separator():
    return os.environ['AUTO_DOCSTRING_OPTION_SEPARATOR']


def get_option_separator():
    return get_config_entry('option_separator', ' or ')


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


register_config_entry('container_prefix', predicate=_get_container_prefix)
register_config_entry('container_suffix', predicate=_get_container_suffix)
register_config_entry('delimiter', predicate=_get_docstring_delimiter)
register_config_entry('indent', predicate=_get_default_indent)
register_config_entry('option_separator', predicate=_get_option_separator)
register_config_entry('raw_prefix', predicate=_auto_raw_prefix)
register_config_entry('style', predicate=_get_current_style)
register_config_entry('type_follow', predicate=_allow_type_follow)
register_config_entry('description_separator', predicate=_get_description_separator)
