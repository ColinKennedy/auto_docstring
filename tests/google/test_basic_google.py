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

    def test_classmethod(self):
        '''A classmethod on a class should not return "cls" as an arg.'''
        code = \
            '''
            class Something(object):
                @classmethod
                def fizz(cls, foo, bar):
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

    def test_instancemethod(self):
        '''A method on a class should not return "self" as an arg.'''
        code = \
            '''
            class Something(object):
                def fizz(self, foo, bar):
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

    def test_staticmethod(self):
        '''A method on a class that should return all of its args.'''
        code = \
            '''
            class Something(object):
                @staticmethod
                def fizz(foo, bar, buzz):
                    {curs}
                    pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                foo ({2}): {3}.
                bar ({4}): {5}.
                buzz ({6}): {7}.

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
            '''\
            {1}.

            Args:
                bar ({2|int}, optional): {3}.

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
            '''\
            {1}.

            Args:
                something ({2}): {3}.
                another ({4|int}, optional): {5}.

            Returns:
                {6|bool}: {7}.

            '''

        self.compare(expected_output, code)

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
            {1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            '''

        self.compare(expected_output, code)

    def test_kwarg(self):
        code = \
            '''
            def foo(*fizz, **bar):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                *fizz ({2|tuple}, optional): {3}.
                **bar ({4|dict}, optional): {5}.

            '''

        self.compare(expected_output, code)


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

    def test_nested_single_type(self):
        '''Make a docstring that contains a container of only one object-type.'''
        code = \
            '''
            def foo(bar):
                {curs}
                return ['8', '234', '123151', '134.fasfdasd']
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            Returns:
                {4|list[str]}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_return(self):
        '''Make a docstring that is a nested container.'''
        code = \
            '''
            def foo(bar):
                {curs}
                return [['8'], ['8'], ['9'], ['12312']]
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            Returns:
                {4|list[list[str]]}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_multi(self):
        '''Make a docstring for a nested container with more than one type.'''
        code = \
            '''
            def foo(bar):
                {curs}
                return [('8', ), ('8', ), ('9', ), (12312.0, )]
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            Returns:
                {4|list[tuple[str or float]]}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_multi_001(self):
        '''Make a docstring for a nested container with more than one type.'''
        code = \
            '''
            def foo(bar):
                {curs}
                return [('8', ), ['8'], ('9', ), (12312.0, )]
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2}): {3}.

            Returns:
                {4|list[tuple[str or float] or list[str]]}: {5}.

            '''
        self.compare(expected_output, code)

    def test_multi_return_single_type(self):
        '''Build a docstring that has one return type but multiple returns.'''
        code = \
            '''
            import collections

            def some_function(something=collections.OrderedDict):
                {curs}
                if something:
                    return True
                return False

            '''

        expected_output = \
            '''\
            {1}.

            Args:
                something ({2|<collections.OrderedDict>}, optional): {3}.

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
            import collections

            def foo(bar=collections.OrderedDict()):
                {curs}
                if bar:
                    yield True
                yield []
            '''

        expected_output = \
            '''\
            {1}.

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
            import collections

            def an_outer_function(*args, **kwargs):
                def inner_function(bar=collections.OrderedDict()):
                    {curs}
                    if something:
                        yield True
                    yield []
            '''

        expected_output = \
            '''\
            {1}.

            Args:
                bar ({2|<collections.OrderedDict>}, optional): {3}.

            Yields:
                {4|bool or list}: {5}.

            '''
        self.compare(expected_output, code)

    def test_nested_outer_function(self):
        '''Make sure that nested functions don't affect the created docstring.'''
        code = \
            '''
            import collections

            def parent_function(foo='asfd'):
                {curs}
                def inner_function(bar=collections.OrderedDict()):
                    if bar:
                        yield True
                    yield []

                return True
            '''

        expected_output = \
            '''\
            {1}.

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

    def test_imported_class(self):
        '''Build a docstring that has to "find" the class object.'''
        code = \
            '''
            from collections import Counter

            def foo():
                {curs}
                return Counter()
            '''

        expected_output = '{1|<collections.Counter>}: {2}.'

        self.compare(expected_output, code)

    # TODO : Finish these
    # def test_imported_thirdparty_function(self):
    #     '''Build a docstring that has to "find" the function object.'''
    #     code = \
    #         '''
    #         from inspection import dirgrep

    #         def foo():
    #             {curs}
    #             return dirgrep
    #         '''

    #     expected_output = '{1|<inspection.dirgrep>}: {2}.'
    #     self.compare(expected_output, code)

#     def test_imported_thirdparty_class(self):
#         '''Build a docstring that has to "find" the class object.'''
#         code = \
#             '''
#             from auto_docstring.visit import Visitor

#             def foo():
#                 {curs}
#                 return Visitor()
#             '''

#         expected_output = '{1|<auto_docstring.visit.Visitor>}: {2}.'
#         self.compare(expected_output, code)

