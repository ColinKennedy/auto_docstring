#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from . import environment


def get_code_style(name):
    styles = environment.get_style_info()
    try:
        return styles[name]
    except KeyError:
        raise ValueError('Style: "{name}" was invalid. Options were, "{options}".'
                         ''.format(name=name, options=sorted(styles.keys())))


def create_code_style(name, *args, **kwargs):
    style = get_code_style(name)
    return style
