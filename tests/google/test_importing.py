#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import tempfile
import textwrap
import sys
import os

# IMPORT LOCAL LIBRARIES
from .. import common


class TypeTestCase(common.CommonTestCase):
    def test_custom_standard_object(self):
        '''Build a standard-library object that needs to be imported.'''
        code = \
            '''
            import collections

            def foo(bar=collections.OrderedDict()):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2:<collections.OrderedDict>!f}, optional): {3!f}.

            '''

        self.compare(expected_output, code)

    def test_function(self):
        '''Build a docstring that has to "find" the function object.'''
        code = \
            '''
            from itertools import islice

            def foo():
                {curs}
                return islice([4, 5, 6, 7, 8, 9], 3)
            '''

        expected_output = '{1:<itertools.islice>!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_class(self):
        '''Build a docstring that has to "find" the class object.'''
        code = \
            '''
            from collections import Counter

            def foo():
                {curs}
                return Counter()
            '''

        expected_output = '{1:<collections.Counter>!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_third_party_callable_001(self):
        '''Get the full import path because the module is find-able.'''
        code = \
            '''
            from PySide import QtGui

            def make_parser_validator():
                {curs}
                name_regex = parser.get_token_parse(name, parse_type='regex')
                return QtGui.QRegExpValidator(QtCore.QRegExp(name_regex), parent=parent)
            '''

        expected_output = '{1:<PySide.QtGui.QRegExpValidator>!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_third_party_callable_002(self):
        '''Get the direct object because the module is not find-able.'''
        code = \
            '''
            def make_parser_validator():
                {curs}
                name_regex = parser.get_token_parse(name, parse_type='regex')
                return QtGui.QRegExpValidator(QtCore.QRegExp(name_regex), parent=parent)
            '''

        expected_output = '{1:<QtGui.QRegExpValidator>!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_unknown_function(self):
        '''Return a function return type if its type was not found.'''
        code = \
            '''\
            from itertools import izip

            def pairwise(iterable):
                {curs}
                a, b = tee(iterable)
                next(b, None)
                return izip(a, b)
            '''
        expected_output = \
            '''\
            {1!f}.

            Args:
                iterable ({2!f}): {3!f}.

            Returns:
                {4:<itertools.izip>!f}: {5!f}.

            '''
        self.compare(expected_output, code)

    def test_function_001(self):
        '''Create a docstring for an imported function.'''
        code = \
            '''
            from functools import partial

            def wraps(wrapped):
                {curs}
                return partial(update_wrapper, wrapped=wrapped,
                            assigned=assigned, updated=updated)
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                wrapped ({2!f}): {3!f}.

            Returns:
                {4:<functools.partial>!f}: {5!f}.

            '''

        self.compare(expected_output, code)

    def test_function_002(self):
        '''Create a docstring for an imported module with an alias.'''
        code = \
            '''
            import functools as func

            def wraps(wrapped):
                {curs}
                return func.partial(
                    update_wrapper, wrapped=wrapped,
                    assigned=assigned, updated=updated)
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                wrapped ({2!f}): {3!f}.

            Returns:
                {4:<functools.partial>!f}: {5!f}.

            '''

        self.compare(expected_output, code)

    def test_relative_import(self):
        # Create the temporary Python package and set it up with files
        temporary_directory = os.path.join(tempfile.mkdtemp(), 'fake_project')
        # self.files_folders.add(temporary_directory)

        os.makedirs(temporary_directory)
        open(os.path.join(temporary_directory, '__init__.py'), 'w').close()
        sys.path.append(os.path.dirname(temporary_directory))

        foo_code = textwrap.dedent(
            '''\
            class Thing(object):
                @classmethod
                def fizz(cls):
                    return 8

            ''')

        with open(os.path.join(temporary_directory, 'foo.py'), 'w') as file_:
            file_.write(foo_code)

        code = textwrap.dedent(
            '''\
            from . import foo

            def bar():
                {curs}
                return foo.Thing.fizz()
            ''')

        with tempfile.NamedTemporaryFile(delete=False, dir=temporary_directory, suffix='.py') as file_:
            file_.write(code.format(curs=''))
            source_file_path = file_.name

        expected_output = '{1:int!f}: {2!f}.'

        self.compare(expected_output, code)

#     def test_relative_inner_import(self):
#         pass

#     def test_relative_parent_import(self):
#         pass

    # def test_relative_import_unknown(self):
    #
#     def test_relative_inner_import_unknown(self):
#         pass

#     def test_relative_parent_import_unknown(self):
#         pass

