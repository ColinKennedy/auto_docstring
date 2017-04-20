#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest
import abc

# IMPORT THIRD-PARTY LIBRARIES
# TODO : Make relative
import docstring
import common
import parse


# class FindBlockAbstractInterface(object):

#     __metaclass__ = abc.ABCMeta

#     @abc.abstractmethod
#     def test_get_no_args(self):
#         '''Find information for our docstring but get nothing.'''
#         pass

#     @abc.abstractmethod
#     def test_get_one_arg(self):
#         pass

#     @abc.abstractmethod
#     def test_get_multiple_args(self):
#         pass

#     @abc.abstractmethod
#     def test_get_args_and_return(self):
#         pass

#     @abc.abstractmethod
#     def test_get_args_and_yield(self):
#         pass


# class FindFunctionDirectionBothInfoTestCase(common.CommonTestCase,
#                                             unittest.TestCase):
#     def test_get_no_args(self):
#         '''Find information for our docstring but get back nothing.'''
#         # Mimic the Vim buffer by splitting some function into a list of strs
#         some_function = \
#             '''\
#             def some_function():
#                 {curs}
#                 pass
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_args()), 0)

#     def test_get_one_arg(self):
#         some_function = \
#             '''\
#             def some_function(something):
#                 {curs}
#                 pass
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_args()), 1)

#     def test_get_multiple_args(self):
#         some_function = \
#             '''\
#             def some_function(something, another):
#                 {curs}
#                 pass
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_args()), 2)

#     def test_get_kwargs(self):
#         some_function = \
#             '''\
#             def some_function(kwarg_thing='asfasd'):
#                 {curs}
#                 pass
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_kwargs()), 1)

#     def test_get_args_and_return(self):
#         some_function = \
#             '''\
#             def some_function(kwarg_thing='asfasd'):
#                 {curs}
#                 return True
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_returns()), 1)

#     def test_get_multi_returns_same_type(self):
#         '''Parse the 'single-type' return for one function.

#         Frequently, functions may return False or True. This function will
#         get all return types and, if the type of more than one return is
#         the same, it should only display that one type.

#         '''
#         some_function = \
#             '''\
#             def some_function(kwarg_thing='asfasd'):
#                 {curs}
#                 if something:
#                     return True
#                 return False
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_returns()), 2)
#         self.assertEqual(block_info.get_returns_types(), ['bool'])

#     def test_get_multi_returns_different_types(self):
#         '''Parse the 'multi-type' return for one function.

#         Some functions return more than one type of object
#         (usually, something or NoneType). Get all the return options and
#         their return types.

#         '''
#         some_function = \
#             '''\
#             def some_function(kwarg_thing='asfasd'):
#                 {curs}
#                 if something:
#                     return True
#                 return ''
#             '''.format(curs=self.cursor.pointer)
#         some_function = textwrap.dedent(some_function)
#         some_function = some_function.split('\n')
#         row, _ = self.cursor.get_position(some_function)

#         block_info = docstring.get_docstring_raw_info(
#             lines=some_function, row=row)
#         self.assertEqual(len(block_info.get_returns()), 2)
#         self.assertEqual(block_info.get_returns_types(), ['bool', 'str'])

#     def test_get_returns_third_party(self):
#         '''Get the object's type, even if it comes from an imported module.

#         This method is contingent on the idea that the PYTHONPATH for Vim
#         would be the same as the code that is being executed (virtualenv!).

#         '''
#         pass

#     def test_get_returns_third_party_failure(self):
#         '''Try to get the third-party type and fallback if it cannot be found.'''
#         pass

#     def test_get_args_and_yield(self):
#         '''Instead of return of a function, get the yield of a generator.'''
#         pass


# class FindMethodDiectionBothInfoTestCase(common.CommonTestCase,
#                                          unittest.TestCase):
#     def test_get_no_args(self):
#         '''Find information for our docstring but get nothing.'''
#         pass

#     def test_get_one_arg(self):
#         pass

#     def test_get_multiple_args(self):
#         pass

#     def test_get_args_and_return(self):
#         pass

#     def test_get_args_and_yield(self):
#         pass


# class FindClassDirectionBothInfoTestCase(unittest.TestCase):

#     '''Get a Python class definition.'''

#     def test_no_attributes(self):
#         pass

#     def test_one_attribute(self):
#         pass

#     def test_multiple_attibutes(self):
#         pass


if __name__ == '__main__':
    print(__doc__)

