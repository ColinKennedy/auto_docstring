#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests for Google-style function docstrings.'''

# IMPORT LOCAL LIBRARIES
from .. import common


class FunctionTestCase(common.CommonTestCase):

    '''Test different function docstrings.'''

    def test_no_arg(self):
        '''Make a function docstring with no args.'''
        code = \
            '''
            def foo():
                {curs}
                pass
            '''

        expected_output = '''{1}.'''
        self.compare(expected_output, code)

    def test_one_arg(self):
        '''Make a function with one arg.'''
        code = \
            '''
            def foo(bar):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            '''

        self.compare(expected_output, code)

    def test_multiple_args(self):
        '''Test a function with 2 args.'''
        code = \
            '''
            def fizz(foo, bar):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                foo ({2}): {3}.
                bar ({4}): {5}.

            '''
        self.compare(expected_output, code)


class FunctionDefaultArgTestCase(common.CommonTestCase):

    '''Test different functions with default args.'''

    def test_one_optional_arg(self):
        '''Create a docstring that has one, optional arg.'''
        code = \
            '''
            def foo(bar=8):
                {curs}
                pass
            '''

        expected_output = \
            '''{1}.

            Args:
                bar ({2|int}): {3}.

            '''

        self.compare(expected_output, code)

    def test_mixed_args(self):
        '''Make a docstring that has one positional arg and an optional arg.'''
        code = \
            '''
            def some_function(something, another=8):
                {curs}
                return True
            '''

        expected_output = \
            '''{1}.

            Args:
                something ({2}): {3}.
                another ({4|int}, optional): {5}.

            Returns:
                bool: {6}.

            '''

        self.compare(expected_output, code)

    def test_custom_standard_object(self):
        '''Build a standard-library object that needs to be imported.'''
        code = \
            '''
            def foo(bar=collections.OrderedDict()):
                {curs}
                pass
            '''

        expected_output = \
            '''{1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            '''

        self.compare(expected_output, code)

    def test_imported_function(self):
        '''Build a docstring that has to "find" the function object.'''
        code = \
            '''
            from itertools import islice

            def foo():
                {curs}
                return islice([4, 5, 6, 7, 8, 9], 3)
            '''

        expected_output = '{1|<itertools.islice>}: {2}.'

        self.compare(expected_output, code)

    # TODO : third-party (importable)
    # get the type from an imported class
    # get the type from an imported function
    # no return-type - can't figure it out


class ReturnTestCase(common.CommonTestCase):

    '''Test different return statement scenarios.'''

    def test_builtin_object_single(self):
        '''Make a docstring to describe a function that has a return value.'''
        code = \
            '''
            def foo():
                {curs}
                return True
            '''

        expected_output = '{1|bool}: {2}.'''
        self.compare(expected_output, code)

    def test_builtin_object_multiline(self):
        '''Make a docstring to describe a function that has a return value.'''
        code = \
            '''
            def foo(bar):
                {curs}
                return True
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            Returns:
                {4|bool}: {5}.

            '''
        self.compare(expected_output, code)

    def test_multi_return_single_type(self):
        '''Build a docstring that has one return type but multiple returns.'''
        code = \
            '''
            def some_function(something=collections.OrderedDict):
                {curs}
                if something:
                    return True
                return False

            '''

        expected_output = \
            '''{1}.

            Args:
                some_arg ({2|<collections.OrderedDict>}, optional): {3}.

            Returns:
                {4|bool}: {5}.

            '''

        self.compare(expected_output, code)

    def test_multi_return(self):
        '''Make a docstring to describe a function that has two return values.'''
        code = \
            '''
            import collections


            def foo(bar=collections.OrderedDict()):
                {curs}
                if bar:
                    return True
                return ''

            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            Returns:
                {4|bool or str}: {5}.

            '''
        self.compare(expected_output, code)

    def test_multi_yield(self):
        '''Make a docstring to describe a function that has a yield value.'''
        code = \
            '''
            def foo(bar=collections.OrderedDict()):
                {curs}
                if bar:
                    yield True
                yield []
            '''

        expected_output = \
            '''{1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            Yields:
                {4|bool or list}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_function(self):
        '''Make sure that nested functions return the correct docstring.'''
        code = \
            '''
            def an_outer_function(*args, **kwargs):
                def inner_function(bar=collections.OrderedDict()):
                    {curs}
                    if something:
                        yield True
                    yield []
            '''

        expected_output = \
            '''{1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            Yields:
                {4|bool or list}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_function_outer_function(self):
        '''Make sure that nested functions don't affect the created docstring.'''
        code = \
            '''
            def parent_function(foo='asfd'):
                {curs}
                def inner_function(bar=collections.OrderedDict()):
                    if bar:
                        yield True
                    yield []

                return True
            '''

        expected_output = \
            '''{1}.

            Args:
                foo ({2|str}, optional): {3}.

            Returns:
                {4|bool}: {5}.

            '''
        self.compare(expected_output, code)

    # def test_function_with_unknown_return(self):
    #     '''Return a function return type if its type was not found.'''
    #     code = \
    #         '''\
    #         def pairwise(iterable):
    #             {curs}
    #             a, b = tee(iterable)
    #             next(b, None)
    #             return izip(a, b)
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             iterable ({2}): {3}.

    #         Returns:
    #             {4:izip}: {5}.

    #         '''
    #     self.compare(expected_output, code)

