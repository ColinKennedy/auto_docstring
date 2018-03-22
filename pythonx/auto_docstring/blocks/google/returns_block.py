#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The class and functions needed to print a Google-style "Returns:" block.'''

# IMPORT LOCAL LIBRARIES
from . import common_block


class Returns(common_block.MultiTypeBlock):

    '''The "Returns:" block main class.'''

    label = 'Returns'
    name = 'returns'
    _info_key = name
