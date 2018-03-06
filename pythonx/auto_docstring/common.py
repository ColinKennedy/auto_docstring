#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os
import re
import csv


OPTIONS = {
    'style': os.getenv('AUTO_DOCSTRING_STYLE', 'google'),
}
_STYLES = dict()
_STYLE_BLOCK_ORDER_COMPILE = re.compile('(?P<name>\w+):(?P<blocks>[\w+,])')


def register_code_style(name, obj):
    _STYLES[name] = obj


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


def get_code_style(name):
    try:
        return _STYLES[name]
    except KeyError:
        raise ValueError('Style: "{name}" was invalid. Options were, "{options}".'
                         ''.format(name=name, options=sorted(_STYLES.keys())))


def get_default_indent():
    return os.getenv('AUTO_DOCSTRING_INDENT', '    ')


def create_code_style(name, *args, **kwargs):
    style = get_code_style(name)
    return style
