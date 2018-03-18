#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests for Google-style function docstrings.'''

# IMPORT AUTO-DOCSTING LIBRARIES
import auto_docstring

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

    # def test_implicit_if_001(self):
    #     code = self._make_code(
    #         '''
    #         def add_docstring(code, row, style='', mode='replace'):
    #             %s
    #             code = list(code)
    #             docstring = create_docstring(code=code, row=row, style=style)

    #             if mode == 'replace':
    #                 raise NotImplementedError('Need to write this')
    #                 # code[row:] = docstring
    #             elif mode == 'insert':
    #                 code.insert(row, docstring)
    #             else:
    #                 options = ('replace', 'insert')
    #                 raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
    #                                 ''.format(mode=mode, options=options))

    #             return code

    #         ''')

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Args:
    #             code ({2!f}): {3!f}.
    #             row ({4!f}): {5!f}.
    #             style ({6:str!f}, optional): {7!f}.
    #             mode ({8:str!f}, optional): {9!f}.
    #                 "insert" - {10!f}.
    #                 "replace" - {11!f}.

    #         Raises:
    #             NotImplementedError:
    #             ValueError: Mode: "{mode}" is unsupported. Options were, "{options}".'

    #         Returns:
    #             list:

    #         '''

    #     self.compare(expected_output, code)

    # def test_implicit_if_002(self):
    #     code = self._make_code(
    #         '''
    #         def add_docstring(code, row, style='', mode='replace'):
    #             %s
    #             code = list(code)
    #             docstring = create_docstring(code=code, row=row, style=style)

    #             if mode == 'replace':
    #                 raise NotImplementedError('Need to write this')
    #                 # code[row:] = docstring

    #             mode = False
    #             if mode == 'insert':
    #                 code.insert(row, docstring)
    #             else:
    #                 options = ('replace', 'insert')
    #                 raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
    #                                 ''.format(mode=mode, options=options))

    #             return code

    #         ''')

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Args:
    #             code ({2!f}): {3!f}.
    #             row ({4!f}): {5!f}.
    #             style ({6:str!f}, optional): {7!f}.
    #             mode ({8:str!f}, optional): {9!f}.
    #                 "replace" - {10!f}.

    #         Raises:
    #             NotImplementedError:
    #             ValueError: Mode: "{mode}" is unsupported. Options were, "{options}".'

    #         Returns:
    #             list:

    #         '''

    #     self.compare(expected_output, code)


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


class StandardTestCase(common.CommonTestCase):

    '''A test case for built-in objects and standard library objects.'''

    def test_object_single(self):
        '''Make a docstring to describe a function that has a return value.'''
        code = \
            '''
            def foo():
                {curs}
                return True
            '''

        expected_output = '{1:bool!f}: {2!f}.'''
        self.compare(expected_output, code)

    def test_object_multiline(self):
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

    def test_double_line(self):
        code = \
            '''
            def foo():
                {curs}
                fum, bar = [8, 9]
                return fum
            '''

        expected_output = '{1:int!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_callable_type(self):
        code = \
            '''
            def get_info():
                {curs}
                return dict()
            '''

        expected_output = '{1:dict!f}: {2!f}.'

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

    def test_unknown_type_001(self):
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

    def test_unknown_type_002(self):
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

    def test_unknown_type_003(self):
        code = \
            '''
            def wraps(wrapped):
                {curs}
                return foo.bar.partial(
                    update_wrapper, wrapped=wrapped,
                    assigned=assigned, updated=updated)
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                wrapped ({2!f}): {3!f}.

            Returns:
                {4:<foo.bar.partial>!f}: {5!f}.

            '''

        self.compare(expected_output, code)

    def test_unknown_type_004(self):
        code = self._make_code(
            '''
            def make_container_label(container, items_text):
                %s
                if items_text:
                    return '{container}[{items_text}]'.format(
                        container=container, items_text=items_text)

                return container
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                container ({2!f}): {3!f}.
                items_text ({4!f}): {5!f}.

            Returns:
                {6:<str.format> or container!f}: {7!f}.

            '''

        self.compare(expected_output, code)

    # TODO : Make this return list[str]
    def test_known_global_variable(self):
        code = \
            '''
            _STYLES = ['asdfsdf']

            def get_style_info():
                {curs}
                return _STYLES
            '''

        expected_output = '{1:list!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_unknown_global_variable(self):
        '''If we cannot find a Name object's type, return its literal label.'''
        code = \
            '''
            def get_style_info():
                {curs}
                return _STYLES
            '''

        expected_output = '{1:_STYLES!f}: {2!f}.'

        self.compare(expected_output, code)


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

    def test_boolop_001(self):
        code = \
            '''
            def foo():
                {curs}
                return '8' in ['8'] and False in (True, )
            '''

        expected_output = '{1:bool!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_in_statement(self):
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
    def test_basic(self):
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
        code = \
            '''
            def foo():
                {curs}
                return int(uninferreable_object)
            '''

        expected_output = '{1:int!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_object_with_set(self):
        code = \
            '''
            def foo():
                {curs}
                return set(uninferreable_object)
            '''

        expected_output = '{1:set!f}: {2!f}.'

        self.compare(expected_output, code)


class ComprehensionTestCase(common.CommonTestCase):
    def test_list_comp_001(self):
        code = \
            '''
            def foo():
                {curs}
                return ['str' for _ in range(10)]
            '''

        expected_output = '{1:list[str]!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_list_comp_002(self):
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
