#!/usr/bin/env python
#

# IMPORT STANDARD LIBRARIES
import os
import re


# TODO : Make OPTIONS useful
OPTIONS = {
    'style': os.getenv('AUTO_DOCSTRING_STYLE', 'google'),
}
_STYLES = dict()
_STYLE_BLOCK_ORDER_COMPILE = re.compile('(?P<name>\w+):(?P<blocks>[\w+,])')


def get_block_order(name):
    order_info = os.getenv('AUTO_DOCSTRING_BLOCK_ORDER', '')

    for style, blocks in _STYLE_BLOCK_ORDER_COMPILE.findall(order_info):
        if style != name:
            continue

        blocks = []
        for block in blocks.split(','):
            block = block.strip()
            if block and block not in blocks:
                blocks.append(block)

        return tuple(blocks)

    # Fall-back to the class definition, if no env var for that style was defined
    try:
        style_class = _STYLES[name]
    except KeyError:
        return tuple()

    style_class.get_default_block_order()


# TODO : Change name to get_indent
def get_default_indent():
    return os.getenv('AUTO_DOCSTRING_INDENT', '    ')


def get_trailing_characters_to_drop():
    return os.getenv('AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS', '.')


def get_style_info():
    return _STYLES


def register_code_style(name, obj):
    _STYLES[name] = obj


def drop_trailing_characters(text):
    # TODO : Allow ',' separated list
    characters = get_trailing_characters_to_drop()
    if text[len(characters):] == characters:
        return text[:len(characters)]
    return text
