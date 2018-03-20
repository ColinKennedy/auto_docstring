#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test the functions for converting docstrings.

This module tests converting auto_docstring docstrings into UltiSnips docstrings.

'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring.parsing import ultisnips_build
from auto_docstring.parsing import numberify
from auto_docstring import docstring_builder


class UnnumberedToNumberedTestCase(unittest.TestCase):

    '''Convert un-numbered strings into "auto_docstring-recognizable" strings.'''

    def compare(self, docstring, expected_output):
        '''Convert `docstring` and then test if it matches `expected_output`.'''
        formatter = numberify.RecursiveNumberifyParser()
        converted_docstring = formatter.parse(docstring)
        self.assertEqual(converted_docstring, expected_output)

    def test_matching_kwargs(self):
        '''Convert a docstring that has named fields with the same numbers.

        Also, notice that {5!f} is incorrect and is auto-corrected to 4.

        '''
        docstring = textwrap.dedent(
            '''\
            {!f}.

            Args:
                some_arg ({1:int!f}, optional): {!f}.
                another ({1:int!f}, optional): {5!f}.

            ''')

        expected_output = textwrap.dedent(
            '''\
            {1!f}.

            Args:
                some_arg ({2:int!f}, optional): {3!f}.
                another ({2:int!f}, optional): {4!f}.

            ''')

        self.compare(docstring, expected_output)

    def test_mixed_syntax(self):
        '''Convert a docstring that has a variety of syntax.'''
        docstring = textwrap.dedent(
            '''\
            {}.

            Args:
                some_arg ({1:int!f}, optional): {33!f}.
                another ({asdf:int}, optional): {!f}.

            ''')

        expected_output = textwrap.dedent(
            '''\
            {}.

            Args:
                some_arg ({1:int!f}, optional): {2!f}.
                another ({asdf:int}, optional): {3!f}.

            ''')

        self.compare(docstring, expected_output)

    def test_unique_kwargs(self):
        '''Convert a docstring that has named fields with different numbers.'''
        docstring = textwrap.dedent(
            '''\
            {!f}.

            Args:
                some_arg ({1:int!f}, optional): {!f}.
                another ({2:int}, optional): {!f}.

            ''')

        expected_output = textwrap.dedent(
            '''\
            {1!f}.

            Args:
                some_arg ({2:int!f}, optional): {3!f}.
                another ({2:int}, optional): {4!f}.

            ''')

        self.compare(docstring, expected_output)


class NumberedToUltiSnipsTestCase(unittest.TestCase):

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
            {1!f}.

            Args:
                some_arg ({2!f}): {3!f}.

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
            {1!f}.

            Args:
                some_arg ({2!f}): {3!f}.
                another_arg ({4!f}): {5!f}.

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
            {1!f}.

            Args:
                some_arg ({2:int!f}, optional): {3!f}.

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
            {1!f}.

            Args:
                some_arg ({2:int!f}, optional): {3!f}.
                another ({4:<collections.OrderedDict>!f}, optional): {5!f}.

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
            {1!f}.

            Args:
                some_arg ({2:some{thing}here!f}, optional): {3!f}.
                bar ({4:some{5:thing!f}here!f}, optional): {6!f}.

            '''
        expected_output = \
            '''\
            $1.

            Args:
                some_arg (${2:some{thing}here}, optional): $3.
                bar (${4:some${5:thing}here}, optional): $6.

            '''
        self.compare(docstring, expected_output)
