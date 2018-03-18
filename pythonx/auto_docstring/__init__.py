#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import imp
import os

# IMPORT LOCAL LIBRARIES
from . import environment
from .styles import google
from .defaults import registry
from .defaults.registry import register
from .defaults.registry import get_default
from .defaults.registry import deregister_all


environment.register_code_style(
    name='google',
    obj=google.GoogleStyle,
)

# TODO : Split this out into another repo so that the core can be separate from
#        the preset functions/return objects
#
__CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
__PRESETS_DIR = os.path.join(__CURRENT_DIR, 'defaults', 'presets')
for item in os.listdir(__PRESETS_DIR):
    if item == '__init__.py' or item.endswith(('.pyc', '.pyd')):
        continue

    name = os.path.splitext(item)[0]
    full_path = os.path.join(__PRESETS_DIR, item)
    imp.load_source(name, full_path)


__all__ = [
    'register',
    'get_default',
    'deregister_all',
]
