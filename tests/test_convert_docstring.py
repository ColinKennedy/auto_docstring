#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test the functions for converting docstrings.

This module tests converting auto_docstring docstrings into UltiSnips docstrings.

'''

# IMPORT STANDARD LIBRARIES
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring import docstring_builder_two as docstring_builder


class ConvertUltiSnipsSnippet(unittest.TestCase):

    '''Convert docstrings into UltiSnips docstrings.'''

    def compare(self, docstring, expected_output):
        '''Convert `docstring` and then test if it matches `expected_output`.'''
        converted_docstring = docstring_builder.convert_to_ultisnips(docstring)
        self.assertEqual(converted_docstring, expected_output)

    def test_no_args_convert(self):
        '''Test that a docstring with nothing in it does not convert.'''
        docstring = ''
        expected_output = ''
        self.compare(docstring, expected_output)

    def test_arg_convert(self):
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

    def test_multi_args_convert(self):
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

    def test_kwargs_convert(self):
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

    def test_multi_kwargs_convert(self):
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
