#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT STANDARD LIBRARIES
import textwrap
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from dunders import ultisnips_build


class ConvertDocstringToUltiSnipSnippet(unittest.TestCase):
    def compare_and_test_docstrings(self, docstring, expected):
        formatter = ultisnips_build.UltiSnipsTabstopFormatter()
        docstring_output = textwrap.dedent(docstring)
        expected = textwrap.dedent(expected)
        output = formatter.format(docstring_output)
        self.assertEqual(output, expected)

    def test_docstring_no_args_convert(self):
        docstring_output = ''
        expected_output = ''
        self.compare_and_test_docstrings(docstring_output, expected_output)

    def test_docstring_arg_convert(self):
        docstring_output = \
            '''
            {1}.

            Args:
                some_arg ({2}): {3}.

            '''
        expected_output = \
            '''
            $1.

            Args:
                some_arg ($2): $3.

            '''
        self.compare_and_test_docstrings(docstring_output, expected_output)

    def test_docstring_multi_args_convert(self):
        docstring_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.
                another_arg ({4}): {5}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg ($2): $3.
                another_arg ($4): $5.

            '''
        self.compare_and_test_docstrings(docstring_output, expected_output)

    def test_docstring_kwargs_convert(self):
        docstring_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:int}, optional): {3}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:int}, optional): $3.

            '''
        self.compare_and_test_docstrings(docstring_output, expected_output)

    def test_docstring_multi_kwargs_convert(self):
        docstring_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:int}, optional): {3}.
                another ({4:<collections.OrderedDict>}, optional): {5}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:int}, optional): $3.
                another (${4:<collections.OrderedDict>}, optional): $5.

            '''
        self.compare_and_test_docstrings(docstring_output, expected_output)


if __name__ == '__main__':
    print(__doc__)

