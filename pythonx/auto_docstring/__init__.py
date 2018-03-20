#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The main folder for auto_docstring, a tool that creates Python docstrings.

User-defined return types are imported and added to auto_docstring's
collection of known objects/return-objects. Also, google-style is added as
a default-registered code-style.

'''

# IMPORT STANDARD LIBRARIES
import imp
import os

# IMPORT LOCAL LIBRARIES
from .styles import google
from .defaults import registry
from .config import environment
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
# TODO : Also, add a way for people to add their own files/folders
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
