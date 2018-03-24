#!/usr/bin/env python
#

class SphinxBlockMixin(object):

    label = ''

    def get_starting_lines(cls):
        return [cls.label, '-' * len(cls.label)]
