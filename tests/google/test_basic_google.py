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

        expected_output = '''{1!f}.'''
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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

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
            {1!f}.

            Args:
                foo ({2!f}): {3!f}.
                bar ({4!f}): {5!f}.

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
            {1!f}.

            Args:
                foo ({2!f}): {3!f}.
                bar ({4!f}): {5!f}.

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
            {1!f}.

            Args:
                foo ({2!f}): {3!f}.
                bar ({4!f}): {5!f}.

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
            {1!f}.

            Args:
                foo ({2!f}): {3!f}.
                bar ({4!f}): {5!f}.
                buzz ({6!f}): {7!f}.

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
            {1!f}.

            Args:
                bar ({2:int!f}, optional): {3!f}.

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
            {1!f}.

            Args:
                something ({2!f}): {3!f}.
                another ({4:int!f}, optional): {5!f}.

            Returns:
                {6:bool!f}: {7!f}.

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
            {1!f}.

            Args:
                bar ({2:<collections.OrderedDict>!f}, optional): {3!f}.

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
            {1!f}.

            Args:
                *fizz ({2:tuple!f}, optional): {3!f}.
                **bar ({4:dict!f}, optional): {5!f}.

            '''

        self.compare(expected_output, code)

    def test_none(self):
        code = \
            '''
            def foo(bar=None):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2:NoneType!f}, optional): {3!f}.

            '''
        self.compare(expected_output, code)

    def test_nested_multi(self):
        '''Make a docstring for a nested container with more than one type.'''
        code = \
            '''
            def foo(bar=[('8', ), ('8', ), ('9', ), (12312.0, )]):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2:list[tuple[str or float]]!f}, optional): {3!f}.

            '''
        self.compare(expected_output, code)


class ReturnYieldTestCase(common.CommonTestCase):

    '''Test different return statement scenarios.'''

    def test_builtin_object_single(self):
        '''Make a docstring to describe a function that has a return value.'''
        code = \
            '''
            def foo():
                {curs}
                return True
            '''

        expected_output = '{1:bool!f}: {2!f}.'''
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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:bool!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:list[str]!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:list[list[str]]!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:list[tuple[str or float]]!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:list[tuple[str or float] or list[str]]!f}: {5!f}.

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
            {1!f}.

            Args:
                something ({2:<collections.OrderedDict>!f}, optional): {3!f}.

            Returns:
                {4:bool!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2:<collections.OrderedDict>!f}, optional): {3!f}.

            Returns:
                {4:bool or str!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2:<collections.OrderedDict>!f}, optional): {3!f}.

            Yields:
                {4:bool or list!f}: {5!f}.

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
            {1!f}.

            Args:
                bar ({2:<collections.OrderedDict>!f}, optional): {3!f}.

            Yields:
                {4:bool or list!f}: {5!f}.

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
            {1!f}.

            Args:
                foo ({2:str!f}, optional): {3!f}.

            Returns:
                {4:bool!f}: {5!f}.

            '''
        self.compare(expected_output, code)

    def test_yield_with_return(self):
        code = \
            '''
            def generator(value):
                {curs}
                if value == 5:
                    return

                    # some comment
                    """An empty string"""
                    ''
                    yield

                for index in range(10):
                    yield 10
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                value ({2!f}): {3!f}.

            Yields:
                {4:int!f}: {5!f}.

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

        expected_output = '{1:<itertools.islice>!f}: {2!f}.'

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

        expected_output = '{1:<collections.Counter>!f}: {2!f}.'

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

#     def test_uninferrable_001(self):
#         code = \
#             """
#             def foo():
#                 {curs}
#                 for value in range(10):
#                     yield value
#             """

#         expected_output = '''{1<value>!f}: {2!f}.'''

#         self.compare(expected_output, code)


class DictTestCase(common.CommonTestCase):
    def test_basic(self):
        code = self._make_code(
            '''
            def foo(bar):
                %s
                return {'asfdsf': 8, 'tttt': 123}
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:dict[str, int]!f}: {5!f}.

            '''
        self.compare(expected_output, code)

    def test_basic_multi_type(self):
        code = self._make_code(
            '''
            def foo(bar):
                %s
                return {'asfdsf': 8, False: 123.456}
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:dict[str or bool, int or float]!f}: {5!f}.

            '''
        self.compare(expected_output, code)

    def test_layered_type(self):
        code = self._make_code(
            '''
            def foo(bar):
                %s
                return {('tasdf', 'astsdf', {False: True}): 8, False: 123.456}
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Returns:
                {4:dict[tuple[str or dict[bool, bool]] or bool, int or float]!f}: {5!f}.

            '''
        self.compare(expected_output, code)


class TypesTestCase(common.CommonTestCase):
    def test_compare(self):
        code = \
            """
            def is_valid():
                {curs}
                return column == 0
            """

        expected_output = '{1:bool!f}: {2!f}.'

        self.compare(expected_output, code)
