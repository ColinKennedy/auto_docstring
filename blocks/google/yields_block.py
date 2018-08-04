#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Google-style "Yields:" block.'''

# IMPORT LOCAL LIBRARIES
from . import common_block


class Yields(common_block.MultiTypeBlock):

    '''The "Yields:" block main class.'''

    label = 'Yields'
    name = 'yields'
    _info_key = name
