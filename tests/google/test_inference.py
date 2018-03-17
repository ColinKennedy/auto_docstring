#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test the ways that auto_docstring finds object types.'''

# IMPORT LOCAL LIBRARIES
from .. import common


class RecursionTestCase(common.CommonTestCase):
    def test_other_function(self):
        code = \
            '''
            def foo(arg1):
                if arg1:
                    return 8
                return 'something'

            def bar():
                {curs}
                return foo()

            '''

        expected_output = '{1:int or str!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_other_nested_function(self):
        code = \
            '''
            def foo(arg1):
                if arg1:
                    return 8
                return 'something'

            def bar():
                return foo()

            def fizz():
                {curs}
                return bar()
            '''

        expected_output = '{1:int or str!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_other_nested_function_002(self):
        code = \
            '''
            def foo(arg1):
                if arg1:
                    return 8
                return 'something'

            def bar(arg2):
                if arg2:
                    return 10.9
                return foo()

            def fizz():
                {curs}
                return bar()
            '''

        expected_output = '{1:float or int or str!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_other_nested_function_002(self):
        code = \
            '''
            def foo(arg1):
                if arg1:
                    return 8
                return 'something'

            def bar(arg2):
                if arg2:
                    return 10.9
                return foo()

            def fizz():
                {curs}
                return bar()
            '''

        expected_output = '{1:float or int or str!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_nested_function_003(self):
        '''Test that docstrings are correct when functions are revered.'''
        code = \
            '''
            def foo(arg1):
                if arg1:
                    return 8
                return 'something'

            def fizz():
                {curs}
                return bar()

            def bar(arg2):
                if arg2:
                    return 10.9
                return foo()
            '''

        expected_output = '{1:float or int or str!f}: {2!f}.'

        self.compare(expected_output, code)


    def test_classmethod(self):
        code = \
            '''
            class Foo(object):
                def bar():
                    return 'str'

            def fizz():
                {curs}
                return Foo.bar()
            '''

        expected_output = '{1:float or int or str!f}: {2!f}.'

        self.compare(expected_output, code)
