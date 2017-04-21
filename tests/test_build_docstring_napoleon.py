#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''All tests for building docstrings, in a variety of code scenarios.'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest
import abc

# IMPORT THIRD-PARTY LIBRARIES
from docstring_python import class_read
import common


class FunctionTestAbstractInterface(object):

    '''Make sure that all function tests support the minimum-required tests.'''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def test_build_docstring_no_args(self):
        '''Make a docstring that is just a summary line.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_one_arg(self):
        '''Make a function docstring that has one positional arg.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_multi_args(self):
        '''Build docstrings for functions with more than one positional arg.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg(self):
        '''Create a docstring that has default arg info.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg_custom(self):
        '''Build a docstring that has a default arg that is not built in.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg_statement(self):
        '''Make a function docstring that prefers a built-in statement.

        For example, if the default arg is a bool or NoneType, the text that
        the docstring changes from 'Default: X' to 'Default is X'.

        '''
        pass

    @abc.abstractmethod
    def test_build_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        pass

    @abc.abstractmethod
    def test_build_yield_docstring(self):
        '''.'''
        pass


class CommonFunctionTestCase(common.CommonTestCase):

    '''A simple unittest that has some brief helper methods.

    Keep test code short.

    '''

    def get_docstring(self, input_text):
        '''<docstring.PythonGoogleDocstring>: The docstring for this text.'''
        input_text = input_text.format(curs=self.cursor.pointer)
        input_text = textwrap.dedent(input_text)
        row, _ = self.cursor.get_position(input_text.split('\n'))

        return class_read.create_auto_docstring(
            code=input_text, row=row, language='python', style='google')

    def compare_docstring_with_output(self, input_text, expected_output):
        '''Compare the docstring that the input creates with the expected.

        Args:
            input_text (list[str]): The input text.
            expected_output (str): The output docstring that input_text
                                   should make.

        '''
        docs = self.get_docstring(input_text)
        expected_output = textwrap.dedent(expected_output)
        self.assertEqual(docs, expected_output)


class BuildFunctionDocstringTestCase(CommonFunctionTestCase, unittest.TestCase):

    '''Create docstrings for a napoleon-style function.'''

    def test_build_docstring_no_args(self):
        '''Make a docstring that is just a summary line.'''
        pass

    def test_build_docstring_one_arg(self):
        '''Make a function docstring that has one positional arg.'''
        some_function = \
            '''\
            def some_function(some_arg):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_multi_args(self):
        '''Build docstrings for functions with more than one positional arg.'''
        some_function = \
            '''\
            def some_function(some_arg, another_arg):
                {curs}
                pass
            '''.format(curs=self.cursor.pointer)
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.
                another_arg ({4}): {5}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_default_arg(self):
        '''Create a docstring that has default arg info.'''
        some_function = \
            '''\
            def some_function(some_arg=8):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:int}): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    # def test_build_docstring_default_arg_custom(self):
    #     '''Build a docstring that has a default arg that is not built in.'''
    #     some_function = \
    #         '''\
    #         def some_function(some_arg=collections.OrderedDict()):
    #             {curs}
    #             pass
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_docstring_default_arg_statement(self):
    #     '''Make a function docstring that prefers a built-in statement.

    #     For example, if the default arg is a bool or NoneType, the format of
    #     the default text is 'Default is X'.

    #     '''
    #     pass

    # def test_build_return_docstring(self):
    #     '''Make a docstring to describe a function that has a return value.'''
    #     some_function = \
    #         '''\
    #         def some_function(some_arg=collections.OrderedDict()):
    #             {curs}
    #             return True
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_return_single_type(self):
    #     '''Build a docstring that has one return type but multiple returns.'''
    #     some_function = \
    #         '''\
    #         def some_function(some_arg=collections.OrderedDict()):
    #             {curs}
    #             if something:
    #                 return True
    #             return False

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_return_docstring(self):
    #     '''Make a docstring to describe a function that has a return value.'''
    #     some_function = \
    #         '''\
    #         def some_function(some_arg=collections.OrderedDict()):
    #             {curs}
    #             if something:
    #                 return True
    #             return ''

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool or str: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_yield_docstring(self):
    #     '''Make a docstring to describe a function that has a yield value.'''
    #     some_function = \
    #         '''\
    #         def some_function(some_arg=collections.OrderedDict()):
    #             {curs}
    #             if something:
    #                 yield True
    #             yield []

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Yields:
    #             bool or list: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # # def test_nested_function_returns(self):
    # #     '''Do not pick up return lines from a nested function.'''
    # #     some_function = \
    # #         '''\
    # #         def a_parent_wrapped_func(yyy='asfd'):
    # #             {curs}
    # #             def some_function(some_arg=collections.OrderedDict()):
    # #                 if something:
    # #                     yield True
    # #                 yield []
    # #             return True

    # #         '''.format(curs=self.cursor.pointer)
    # #     some_function = textwrap.dedent(some_function)
    # #     some_function = some_function.split('\n')
    # #     row, _ = self.cursor.get_position(some_function)

    # #     docs = docstring.get_docstring(lines=some_function, row=row)
    # #     expected_output = \
# # '''{1}.

# # Args:
    # # yyy ({str}): {2}.

# # Yields:
    # # bool: {3}.

# # '''
    # #     expected_output = textwrap.dedent(expected_output)
    # #     self.assertEqual(docs.get_docstring(), expected_output)

    # def test_build_return_docstring_implicit(self):
    #     '''Create a docstring where one or more bare return is used.'''
    #     pass

    # def test_build_yield_docstring_implicit(self):
    #     '''Create a docstring where one or more bare yield is used.'''
    #     pass

    # def test_build_docstring_multiline_args(self):
    #     '''Build a function docstring from a definition that is 2+ lines.'''
    #     pass

    # # def test_nested_function_definition(self):
    # #     '''Create a function docstring, even if inside another function.'''
    # #     # some_function = \
    # #     #     '''\
    # #     #     def some_wrapped_function():
    # #     #         def some_function(ttt_arg=collections.OrderedDict()):
    # #     #             {curs}
    # #     #             if something:
    # #     #                 yield True
    # #     #             yield []

    # #     #     '''.format(curs=self.cursor.pointer)
    # #     # some_function = textwrap.dedent(some_function)
    # #     # some_function = some_function.split('\n')
    # #     # row, _ = self.cursor.get_position(some_function)

    # #     # docs = docstring.get_docstring(lines=some_function, row=row)
    # #     # expected_output = \
# # # '''{1}.

# # # Args:
    # # # some_arg ({<collections.OrderedDict>}): {2}.

# # # Yields:
    # # # bool or list: {3}.

# # # '''
    # #     # expected_output = textwrap.dedent(expected_output)
    # #     # self.assertEqual(docs.get_docstring(), expected_output)

    # #     some_function = \
    # #         '''\
    # #         def some_wrapped_function():
    # #             def some_function(ttt_arg=collections.OrderedDict()):
    # #                 {curs}
    # #                 if something:
    # #                     yield True
    # #                 yield []

    # #         '''.format(curs=self.cursor.pointer)
    # #     some_function = textwrap.dedent(some_function)
    # #     some_function = some_function.split('\n')
    # #     row, _ = self.cursor.get_position(some_function)

    # #     funcblock = docstring.get_docstring_raw_info(
    # #         lines=some_function, row=row)
    # #     print('adsfasfd', funcblock.get_parameters())

    # #     docs = docstring.get_docstring(lines=some_function, row=row)
    # #     expected_output = \
# # '''{1}.

# # Args:
    # # some_arg ({<collections.OrderedDict>}): {2}.

# # Yields:
    # # bool or list: {3}.

# # '''


# class BuildMethodDocstringTestCase(CommonFunctionTestCase, unittest.TestCase):

    # '''A suite of docstring test cases for class instancemethods.'''

    # def test_build_docstring_one_arg(self):
    #     '''Create a docstring for a method that takes only one arg.'''
    #     some_function = \
    #         '''\
    #         class SomeClass(object):
    #             def some_function(self, some_arg):
    #                 {curs}
    #                 pass
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({2}): {3}.

    #         '''

    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_docstring_multi_args(self):
    #     '''Build docstrings for functions with more than one positional arg.'''
    #     some_function = \
    #         '''\
    #         class AnotherClass(object):
    #             def some_another_function(self, some_arg, another_arg):
    #                 {curs}
    #                 pass
    #         '''.format(curs=self.cursor.pointer)
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({2}): {3}.
    #             another_arg ({4}): {5}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_docstring_default_arg(self):
    #     '''Create a docstring that has default arg info.'''
    #     some_function = \
    #         '''\
    #         class TaskClass(object):
    #             def some_function(self, some_arg=8):
    #                 {curs}
    #                 pass
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({int}): {2}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_docstring_default_arg_custom(self):
    #     '''Build a docstring that has a default arg that is not built in.'''
    #     some_function = \
    #         '''\
    #         class Torch(object):
    #             def some_function(self, some_arg=collections.OrderedDict()):
    #                 {curs}
    #                 pass
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_return_docstring(self):
    #     '''Make a docstring to describe a function that has a return value.'''
    #     some_function = \
    #         '''\
    #         class Fountain(object):
    #             def some_function(self, some_arg=collections.OrderedDict()):
    #                 {curs}
    #                 return True
    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_return_single_type(self):
    #     '''Build a docstring that has one return type but multiple returns.'''
    #     some_function = \
    #         '''\
    #         class Process(object):
    #             def some_function(self, some_arg=collections.OrderedDict()):
    #                 {curs}
    #                 if something:
    #                     return True
    #                 return False

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_return_docstring(self):
    #     '''Make a docstring to describe a function that has a return value.'''
    #     some_function = \
    #         '''\
    #         class TipTop(object):
    #             def some_function(self, some_arg=collections.OrderedDict()):
    #                 {curs}
    #                 if something:
    #                     return True
    #                 return ''

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Returns:
    #             bool or str: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_build_multi_yield_docstring(self):
    #     '''Make a docstring to describe a function that has a yield value.'''
    #     some_function = \
    #         '''\
    #         class JazzyBoy(object):
    #             def some_function(self, some_arg=collections.OrderedDict()):
    #                 {curs}
    #                 if something:
    #                     yield True
    #                 yield []

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Args:
    #             some_arg ({<collections.OrderedDict>}): {2}.

    #         Yields:
    #             bool or list: {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # def test_method_attribute(self):
    #     '''Add attribute(s) to a method if it is defined out of __init__.'''
    #     some_function = \
    #         '''\
    #         class JazzyBoy(object):
    #             def __init__(self):
    #                 super(JazzyBoy, self).__init__()

    #             def some_function(self):
    #                 {curs}
    #                 self.out_of_init_attribute = 'tt'

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Attributes:
    #             out_of_init_attribute ({str}): {2}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # # def test_method_attribute_init(self):
    # #     '''Add any attribute defined to docstring if method is __init__.'''
    # #     # TODO : Write this test case
    # #     some_function = \
    # #         '''\
    # #         class JazzyBoy(object):
    # #             def __init__(self):
    # #                 super(JazzyBoy, self).__init__()
    # #                 {curs}
    # #                 self.tetsu = 'jin'
    # #                 self.founder = True

    # #         '''
    # #     expected_output = \
    # #         '''\
    # #         {1}.

    # #         Attributes:
    # #             tetsu ({str}): {2}
    # #             founder ({True}): {3}

    # #         '''
    # #     self.compare_docstring_with_output(input_text=some_function,
    # #                                        expected_output=expected_output)

    # def test_method_attribute_multi(self):
    #     '''Append a field for each attribute found.'''
    #     some_function = \
    #         '''\
    #         class JazzyBoy(object):
    #             def __init__(self):
    #                 super(JazzyBoy, self).__init__()

    #             def some_function(self):
    #                 {curs}
    #                 self.out_of_init_attribute = 'tt'
    #                 self.anotherthing = 8

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Attributes:
    #             out_of_init_attribute ({str}): {2}.
    #             anotherthing ({int}): {4}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)


# class BuildClassDocstringTestCase(unittest.TestCase):

    # '''A suite of tests for class-level docstrings.'''

    # # docstring summary line
    # # Attribute
    # # Attributes

    # pass


# class BuildModuleDocstringTestCase(unittest.TestCase):

    # '''A suite of tests for module-level docstrings.'''

    # # Summary line
    # # Attribute
    # # Attributes
    # # Summary lines of classes and docstrings?

    # pass


# if __name__ == '__main__':
    # print(__doc__)

