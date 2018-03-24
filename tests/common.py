#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Simple classes and functions that can be re-used by our unittests.'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest

# IMPORT AUTO-DOCSTING LIBRARIES
from auto_docstring import docstring_builder
import auto_docstring


def get_position(cursor, lines):
    '''Find the given cursor in the given lines of code.

    Args:
        cursor (str): The text to find in `lines`.
        lines (iter[str]): The code that will be searched through.

    Returns:
        tuple[int, int]: The row and column where `cursor` was found in `lines`.

    '''
    row = 0
    column = 0
    for current_row, line in enumerate(lines):
        try:
            current_column = line.index(cursor)
        except ValueError:  #  Happens if index fails
            pass
        else:
            row = current_row
            column = current_column
            break

    return (row, column)


class CommonTestCase(unittest.TestCase):

    '''A unittest.TestCase that makes creating and comparing docstrings easy.'''

    def setUp(self):
        auto_docstring.deregister_all()

    def compare(self, expected_output, code, style='google'):
        '''Format and test the given source `code` and `expected_output`.

        Warning:
            There must be one line in the given `code` that contains "{curs}".
            This line is considered the user's cursor position and will be used
            to generate the docstring.

        Args:
            expected_output (str):
                The docstring that we expect to be returned.
            code (str):
                The source-code that will be used to create a docstring.
            style (`str`, optional):
                The docstring style to use.
                Any key from :func:`auto_docstring.get_all_styles()`
                is valid input for this parameter.

        Raises:
            RuntimeError: If "{curs}" was not found in `code`.

        '''
        expected_output = textwrap.dedent(expected_output)
        code = textwrap.dedent(code)
        try:
            code = self._make_code(code)
        except TypeError:
            # If no %s was in the string, ignore it
            pass

        cursor = '{curs}'
        row, _ = get_position(cursor, code.split('\n'))

        if not row:
            raise RuntimeError(
                'Could not get position. Pointer: "{cursor}" not in code, "{code}".'
                ''.format(cursor=cursor, code=code))

        # Remove the cursor-text and then generate the docstring
        code = code.format(curs='')

        generated_docstring = docstring_builder.create_docstring(code, row=row, style=style)

#         for index, (char1, char2) in enumerate(zip(expected_output, generated_docstring)):
#             if char1 != char2:
#                 raise ValueError(('asdfdf', index, generated_docstring[:index]))

        self.assertEqual(expected_output, generated_docstring)

    @staticmethod
    def _make_code(code):
        code = code.replace('{', '{{').replace('}', '}}')
        return code % '{curs}'
