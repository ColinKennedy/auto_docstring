
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module to test how types are retrieved from strings of Python code.'''

# IMPORT STANDARD LIBRARIES
import collections
import unittest
import ast

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring.code_parser import (get_type, get_type_as_str)


class ReturnVisitor(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super(ReturnVisitor, self).__init__(*args, **kwargs)
        self.returns = []

    def visit_Return(self, node):
        self.returns.append(get_type(node.value, parent=node))


class CommonTypeTestCase(unittest.TestCase):
    def _get_return_type(self, type_str):
        parse = ast.parse(type_str)
        visitor = ReturnVisitor()
        visitor.visit(parse)
        return visitor.returns[0]


class TypeTestCase(CommonTypeTestCase):
    def _test_type(self, type_str, return_type):
        self.assertEqual(self._get_return_type(type_str), return_type)

    def test_importable_class_type(self):
        type_str = 'return collections.defaultdict'
        self._test_type(type_str, collections.defaultdict)

    def test_importable_object(self):
        type_str = 'return collections.defaultdict()'
        self._test_type(type_str, collections.defaultdict)

    def test_built_in_type(self):
        type_str = 'return "asdfsdf"'  # builtin type
        self._test_type(type_str, str)

    def test_known_built_in_function(self):
        type_str = "return ''.join"  # a builtin type with non-obvious syntax
        self._test_type(type_str, str)

    def test_known_method_unknown_object(self):
        # a builtin method on a non-builtin type (class or otherwise)
        type_str = "some_object.split('\n')"

    def test_container_built_in_type(self):
        type_str = "return ['asdf', 'tt']"  # container type
        self._test_type(type_str, [str])

    def test_container_built_in_types(self):
        type_str = "return ['asdfasdf', 8]"  # container type with varying info
        self._test_type(type_str, [str, int])

    def test_container_pairs(self):
        # container type with varying, consistent info
        type_str = "return [(8, 'yyyy'), (8, 'tttt')]"
        self._test_type(type_str, [(int, str)])

    def test_container_triples(self):
        type_str = "return [('adsf', 5, True), ('asdf', 1000, False)]"
        self._test_type(type_str, [(str, int, bool)])

    def test_container_tuple(self):
        type_str = "return (('adsf', 5), ('asdf', 1000))"  # tuple
        self._test_type(type_str, ((str, int),))

    def test_known_built_in_method_0001(self):
        # a builtin method of a bultin type
        type_str = "return 'some thing'.split()"
        self._test_type(type_str, [str])

    def test_known_built_in_method_0002(self):
        # a builtin method of a bultin type
        type_str = "return 'some thing'.replace('asdfasd', 'TT')"
        self._test_type(type_str, str)

    def test_known_built_in_method_0002(self):
        # a builtin method of a bultin type
        type_str = "return ['8'].append('7')"
        self._test_type(type_str, None)

    def test_named_unknown(self):
        type_str = 'return text'  # a named parameter that is defined elsewhere
        self._test_type(type_str, 'text')

    def test_callable_method_0001(self):
        type_str = 'return some.thing()'  # A callable function
        self._test_type(type_str, 'some.thing')

    def test_callable_method_0002(self):
        type_str = 'return os.path.join('')'  # A callable function
        self._test_type(type_str, 'join')

    # def test_known_built_in_method_0001(self):
    #     # a builtin method of a bultin type
    #     type_str = "return 'some\nthing'.split('\n')"
    #     self._test_type(type_str, str)

    # def test_comprehension(self):
    #     type_str = "[('adsf', 5) for _ in range(10)]"  # comprehension

    # def test_callable_method(self):
    #     type_str = 'some.thing()'  # A callable function


class DecomposeTypeTestCase(CommonTypeTestCase):
    def _test_type_str(self, type_str, expected_output):
        found_return_type = self._get_return_type(type_str)
        return_str = get_type_as_str(found_return_type)
        self.assertEqual(return_str, expected_output)

    def test_type_to_str(self):
        type_str = "return 'adsf'"
        self._test_type_str(type_str, 'str')

    def test_known_built_in_method_0001(self):
        # a builtin method of a bultin type
        type_str = "return 'some thing'.split()"
        self._test_type_str(type_str, 'list[str]')

    def test_list_type_to_str(self):
        type_str = "return ['a']"
        self._test_type_str(type_str, 'list[str]')

    def test_nested_list_type_to_str(self):
        type_str = "return [['a']]"
        self._test_type_str(type_str, 'list[list[str]]')

    def test_nested_list_type_to_str(self):
        type_str = "return [['a', 8]]"
        self._test_type_str(type_str, 'list[list[str, int]]')

    def test_nested_list_type_to_str(self):
        type_str = "return [['a', 8, True]]"
        self._test_type_str(type_str, 'list[list[str, int, bool]]')

    def test_nested_list_type_to_str(self):
        type_str = "return ['a', 8, True]"
        self._test_type_str(type_str, 'list[str, int, bool]')

    def test_nested_tuple_type_to_str(self):
        type_str = "return ('a', 8, True)"
        self._test_type_str(type_str, 'tuple[str, int, bool]')


if __name__ == '__main__':
    print(__doc__)

