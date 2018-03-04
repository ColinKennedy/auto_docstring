#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Rebuild strings into UltSnips-compatible snippets.'''

# IMPORT STANDARD LIBRARIES
import string


class UltiSnipsTabstopFormatter(string.Formatter):
    def __init__(self):
        super(UltiSnipsTabstopFormatter, self).__init__()
        self._used_names = dict()
        self._used_numbers = set()

    def get_field(self, field_name, args, kwargs):

        if '|' in field_name:
            label = '${{{}}}'
        else:
            label = '${}'

        label = label.format(field_name)
        label = label.replace('|', ':')
        return (label, field_name)
