#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import unittest


class CursorText(object):
    def __init__(self, pointer):
        super(CursorText, self).__init__()
        self.pointer = pointer

    def get_position(self, lines):
        detected_row_index = 0
        detected_column_index = 0
        for row_index, line in enumerate(lines):
            try:
                char_index = line.index(self.pointer)
            except ValueError:
                pass
            else:
                detected_row_index = row_index
                detected_column_index = char_index
                break

        if not detected_row_index:
            raise RuntimeError('Could not get position. Pointer: "{pnt}" not '
                               'in lines, "{lines}".'
                               ''.format(pnt=self.pointer, lines=lines))

        return (detected_row_index, detected_column_index)


class CommonTestCase(unittest.TestCase):
    def setUp(self):
        '''Create a cursor object that expects a 'X' to mean the position.'''
        self.cursor = CursorText(pointer='X')


if __name__ == '__main__':
    print(__doc__)

