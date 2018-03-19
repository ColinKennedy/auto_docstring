#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests related to the different builtin Python types.'''

# IMPORT LOCAL LIBRARIES
from .. import common


class DictTestCase(common.CommonTestCase):

    '''Test docstrings that have to print a dictionary's keys/values.'''

    def test_basic(self):
        '''Create a basic dict docstring.'''
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
        '''Create a dict docstring that has multiple value types.'''
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
        '''Create a dict docstring with many nested container-types.'''
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

    '''Test different built-in ast node types.'''

    def test_compare(self):
        '''Test that Compare objects return bool.'''
        code = \
            """
            def is_valid():
                {curs}
                return column == 0
            """

        expected_output = '{1:bool!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_boolop_001(self):
        '''Test that BoolOp objects return bool.'''
        code = \
            '''
            def foo():
                {curs}
                return '8' in ['8'] and False in (True, )
            '''

        expected_output = '{1:bool!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_in_statement(self):
        '''Test that __contain__ returns bool.'''
        code = \
            '''
            def foo():
                {curs}
                return '8' in ['8']
            '''

        expected_output = '{1:bool!f}: {2!f}.'

        self.compare(expected_output, code)

    # TODO: Finish this one
    # def test_listcomp(self):
    #     code = \
    #         '''
    #         def foo():
    #             {curs}
    #             return [blah for blah in bar]
    #     '''

    #     expected_output = '{1:list!f}: {2}.'

    #     self.compare(expected_output, code)


class CastTestCase(common.CommonTestCase):

    '''A series of tests for casting objects with built-in type functions.'''

    def test_basic(self):
        '''Test that str() returns str.'''
        code = \
            '''
            def foo():
                {curs}
                thing = some_uninferrable_object
                return str(thing)
            '''

        expected_output = '{1:str!f}: {2!f}.'

        self.compare(expected_output, code)

    # TODO: Finish this one
    # def test_listcomp_with_cast(self):
    #     code = \
    #         '''
    #         def foo():
    #             {curs}
    #             return [str(index) for index in range(10)]
    #     '''

    #     expected_output = '{1:list[str]!f}: {2!f}.'

    #     self.compare(expected_output, code)

    def test_object_with_int(self):
        '''Test that int() returns int.'''
        code = \
            '''
            def foo():
                {curs}
                return int(uninferreable_object)
            '''

        expected_output = '{1:int!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_object_with_set(self):
        '''Test that set() returns set.'''
        code = \
            '''
            def foo():
                {curs}
                return set(uninferreable_object)
            '''

        expected_output = '{1:set!f}: {2!f}.'

        self.compare(expected_output, code)


class ComprehensionTestCase(common.CommonTestCase):

    '''A series of tests for comprehension-syntax, in Python.

    This includes list comprehensions, generator comprehensions, and
    dict comprehensions.

    '''

    def test_list_comp_001(self):
        '''Create a list comphrension docstring.'''
        code = \
            '''
            def foo():
                {curs}
                return ['str' for _ in range(10)]
            '''

        expected_output = '{1:list[str]!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_list_comp_002(self):
        '''Create a list comphrension docstring based on another function.'''
        code = \
            '''
            def bar(arg):
                if arg:
                    return 8

                return 'fizz'

            def foo():
                {curs}
                return [bar(True) for _ in range(10)]
            '''

        expected_output = '{1:list[int or str]!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_nested_list_comp(self):
        '''Create a nested list comphrension docstring.'''
        code = \
            '''
            def bar(arg):
                if arg:
                    return 8

                return 'fizz'

            def foo():
                {curs}
                return [bar(True) for _ in range(10) for _ in range(20)]
            '''

        expected_output = '{1:list[int or str]!f}: {2!f}.'

        self.compare(expected_output, code)

#     def test_generator_comp(self):
#         code = \
#             '''
#             def bar(arg):
#                 if arg:
#                     return 8

#                 return 'fizz'

#             def foo():
#                 {curs}
#                 return set((bar(True) for _ in range(10) for _ in range(20)))
#             '''

#         expected_output = '{1:set[int or str]!f}: {2!f}.'

#         self.compare(expected_output, code)

#     def test_generator_comp_with_function(self):
#         code = \
#             '''
#             def bar(arg):
#                 if arg:
#                     return 8

#                 return 'fizz'

#             def fizz(item):
#                 return tuple(item)

#             def foo():
#                 {curs}
#                 return fizz((bar(True) for _ in range(10) for _ in range(20)))
#             '''

#         expected_output = '{1:tuple[int or str]!f}: {2!f}.'

#         self.compare(expected_output, code)
