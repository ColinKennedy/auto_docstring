#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test the functions for converting docstrings.

This module tests converting auto_docstring docstrings into UltiSnips docstrings.

'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring import numberify
from auto_docstring import docstring_builder_two as docstring_builder


class NumberedToUltiSnips(unittest.TestCase):

    '''Convert docstrings into UltiSnips docstrings.'''

    def compare(self, docstring, expected_output):
        '''Convert `docstring` and then test if it matches `expected_output`.'''
        converted_docstring = docstring_builder.convert_to_ultisnips(docstring)
        self.assertEqual(converted_docstring, expected_output)

    def test_no_args(self):
        '''Test that a docstring with nothing in it does not convert.'''
        docstring = ''
        expected_output = ''
        self.compare(docstring, expected_output)

    def test_arg(self):
        '''Convert a docstring with an arg.'''
        docstring = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg ($2): $3.

            '''
        self.compare(docstring, expected_output)

    def test_multi_args(self):
        '''Convert a docstring with more than one arg.'''
        docstring = \
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
        self.compare(docstring, expected_output)

    def test_kwargs(self):
        '''Convert a docstring with an optional arg.'''
        docstring = \
            '''\
            {1}.

            Args:
                some_arg ({2|int}, optional): {3}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:int}, optional): $3.

            '''
        self.compare(docstring, expected_output)

    def test_multi_kwargs(self):
        '''Convert a docstring with more than one optional args.'''
        docstring = \
            '''\
            {1}.

            Args:
                some_arg ({2|int}, optional): {3}.
                another ({4|<collections.OrderedDict>}, optional): {5}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:int}, optional): $3.
                another (${4:<collections.OrderedDict>}, optional): $5.

            '''
        self.compare(docstring, expected_output)

    def test_nested_braces(self):
        '''Convert a docstring that contains {}s inside of {}s.'''
        docstring = \
            '''\
            {1}.

            Args:
                some_arg ({2|some{thing}here}, optional): {3}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:some{thing}here}, optional): $3.

            '''
        self.compare(docstring, expected_output)


class UnnumberedToUltiSnips(unittest.TestCase):
    def compare(self, docstring, expected_output):
        '''Convert `docstring` and then test if it matches `expected_output`.'''
        formatter = numberify.NumberifyWordFormatter()
        docstring = formatter.format(docstring)
        converted_docstring = docstring_builder.convert_to_ultisnips(docstring)
        self.assertEqual(converted_docstring, expected_output)

    def test_unique_kwargs(self):
        '''Convert a docstring that has named fields with different numbers.'''
        docstring = textwrap.dedent(
            '''\
            {}.

            Args:
                some_arg ({1|int}, optional): {}.
                another ({2|int}, optional): {}.

            ''')

        expected_output = textwrap.dedent(
            '''\
            $1.

            Args:
                some_arg (${2:int}, optional): $3.
                another (${4:int}, optional): $5.

            ''')

        self.compare(docstring, expected_output)

