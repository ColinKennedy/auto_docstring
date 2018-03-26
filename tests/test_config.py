#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import textwrap
import os

# IMPORT LOCAL LIBRARIES
from . import common


class ConfigCommonTestCase(common.CommonTestCase):
    def setUp(self):
        super(ConfigCommonTestCase, self).setUp()
        self.code = \
            """
            # import collections
            import os

            def fizz():
                '''asdfasdfasdfasdf asdf a


                '''
                return collections.OrderedDict()


            def thing(arg):
                '''ifasdfasd.'''
                if arg:
                    return 10.8
                return fizz()

            def bar(arg1, arg2=None, something=(['asdfsd', 8], ('False', ))):
                %s
                if arg1:
                    # return os.getenv('asdfasdf', 10.8)
                    return os.getenv('asdfasdf')

                message = 'Some info. "{thing}"'

                if arg2:
                    raise ValueError(message)

                return thing()

            """

        self.simple_code = \
            '''
            def foo(arg1, arg2=[('asdfads', 10.2, 9), (False, )]):
                {curs}
                if arg1:
                    return 0
                return False
            '''


class BehaviorTestCase(ConfigCommonTestCase):
    def compare_style(self, expected_output, code):
        '''Format and test the given source `code` and `expected_output`.

        Warning:
            There must be one line in the given `code` that contains "{curs}".
            This line is considered the user's cursor position and will be used
            to generate the docstring.

        Args:
            expected_output (str):
                The docstring that we expect to be returned.
            code (str):
                The source-code that will be used to create a docstring.

        Raises:
            RuntimeError: If "{curs}" was not found in `code`.

        '''
        super(BehaviorTestCase, self).compare(expected_output, code, style='')

    def test_default(self):
        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:NoneType!f}, optional): {5!f}.
                something ({6:tuple[list[str or int] or tuple[str]]!f}, optional): {7!f}.

            Raises:
                ValueError: {9:Some info. "{8:thing!f}"!f}.

            Returns:
                {10:<os.getenv> or float or <collections.OrderedDict>!f}: {11!f}.

            '''

        self.compare_style(expected_output, self.code)

    def test_style(self):
        os.environ['AUTO_DOCSTRING_STYLE'] = 'sphinx'

        expected_output = \
            '''\
            {1!f}.

            :param arg1: {2!f}.
            :param arg2: {3!f}.
            :param something: {4!f}.
            :type arg1: {5!f}
            :type arg2: {6:NoneType!f}
            :type something: {7:tuple[list[str or int] or tuple[str]]!f}
            :raises ValueError: {9:Some info. "{8:thing!f}"!f}.
            :returns: {10!f}.
            :rtype: {11:<os.getenv> or float or <collections.OrderedDict>!f}

            '''

        self.compare_style(expected_output, self.code)

    # def test_follow(self):
    #     pass

    # def test_raw_prefix(self):
    #     os.environ['AUTO_DOCSTRING_RAW_PREFIX'] = '0'

    #     code = \
    #         r'''
    #         def foo():
    #             {curs}
    #             raise ValueError('Some message\r')
    #         '''

    #     expected_output = textwrap.dedent(
# '''\
# """{1!f}.

# Raises:
    # ValueError: {2:Some message\r!f}.

# """\
# ''')

    #     self.compare(expected_output, code, wrap=True)

    #     expected_output = 'r' + expected_output
    #     os.environ['AUTO_DOCSTRING_RAW_PREFIX'] = '1'

    #     self.compare(expected_output, code, wrap=True)

    def test_block_order_001(self):
        os.environ['AUTO_DOCSTRING_BLOCK_ORDER'] = 'args,returns,raises'
        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:NoneType!f}, optional): {5!f}.
                something ({6:tuple[list[str or int] or tuple[str]]!f}, optional): {7!f}.

            Returns:
                {8:<os.getenv> or float or <collections.OrderedDict>!f}: {9!f}.

            Raises:
                ValueError: {11:Some info. "{10:thing!f}"!f}.

        '''
        self.compare(expected_output, self.code)

    def test_block_order_001b(self):
        os.environ['AUTO_DOCSTRING_STYLE'] = 'sphinx'
        os.environ['AUTO_DOCSTRING_BLOCK_ORDER'] = 'args,returns,raises'

        expected_output = \
            '''\
            {1!f}.

            :param arg1: {2!f}.
            :param arg2: {3!f}.
            :param something: {4!f}.
            :type arg1: {5!f}
            :type arg2: {6:NoneType!f}
            :type something: {7:tuple[list[str or int] or tuple[str]]!f}
            :returns: {8!f}.
            :rtype: {9:<os.getenv> or float or <collections.OrderedDict>!f}
            :raises ValueError: {11:Some info. "{10:thing!f}"!f}.

            '''

        self.compare_style(expected_output, self.code)

    def test_block_order_001c(self):
        os.environ['AUTO_DOCSTRING_STYLE'] = 'numpy'
        os.environ['AUTO_DOCSTRING_BLOCK_ORDER'] = 'parameters,returns,raises'

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4:NoneType!f}
                {5!f}.
            something : {6:tuple[list[str or int] or tuple[str]]!f}
                {7!f}.

            Returns
            -------
            {8:<os.getenv> or float or <collections.OrderedDict>!f}
                {9!f}.

            Raises
            ------
            ValueError
                {11:Some info. "{10:thing!f}"!f}.

            '''

        self.compare_style(expected_output, self.code)

    def test_block_order_003(self):
        os.environ['AUTO_DOCSTRING_STYLE'] = 'sphinx'
        os.environ['AUTO_DOCSTRING_BLOCK_ORDER'] = 'sphinx:args,returns,raises:'

        expected_output = \
            '''\
            {1!f}.

            :param arg1: {2!f}.
            :param arg2: {3!f}.
            :param something: {4!f}.
            :type arg1: {5!f}
            :type arg2: {6:NoneType!f}
            :type something: {7:tuple[list[str or int] or tuple[str]]!f}
            :returns: {8!f}.
            :rtype: {9:<os.getenv> or float or <collections.OrderedDict>!f}
            :raises ValueError: {11:Some info. "{10:thing!f}"!f}.

            '''

        self.compare_style(expected_output, self.code)


class StyleTestCase(ConfigCommonTestCase):
    def test_delimiter(self):
        os.environ['AUTO_DOCSTRING_DELIMITER'] = "'''"

        code = \
            '''
            def foo():
                {curs}
                return 8
            '''

        expected_output = "'''{1:int!f}: {2!f}.'''"
        self.compare(expected_output, code, wrap=True)

        os.environ['AUTO_DOCSTRING_DELIMITER'] = '"""'

        expected_output = '"""{1:int!f}: {2!f}."""'
        self.compare(expected_output, code, wrap=True)

#     def test_description_separator(self):
#         pass

    def test_include_raise_message(self):
        os.environ['AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE'] = '0'

        code = \
            '''
            def foo():
                {curs}
                raise ValueError('Message')
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {2!f}.

            '''

        self.compare(expected_output, code)

#     def test_remove_trailing_characters(self):
#         pass

#     def test_type_order_001(self):
#         os.environ['AUTO_DOCSTRING_TYPE_ORDER'] = 'ascending'

#         expected_output = \
#             '''\
#             {1!f}.

#             Args:
#                 arg1 ({2!f}): {3!f}.
#                 arg2 ({4:list[tuple[bool or int or float or str]]}): {4!f}.

#             Returns:
#                 {6:bool or int!f}: {7!f}.

#             '''

#         self.compare(expected_output, self.simple_code)

#     def test_type_order_002(self):
#         os.environ['AUTO_DOCSTRING_TYPE_ORDER'] = 'alphabetical'

#         expected_output = \
#             '''\
#             {1!f}.

#             Args:
#                 arg1 ({2!f}): {3!f}.
#                 arg2 ({4:list[tuple[bool or float or int or str]]}): {4!f}.

#             Returns:
#                 {6:bool or int!f}: {7!f}.

#             '''

#         self.compare(expected_output, self.simple_code)

    def test_description_separator(self):
        code = \
            '''
            def foo(arg1):
                {curs}
                return 8
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.

            Returns:
                {4:int!f}: {5!f}.

            '''

        self.compare(expected_output, code)

        os.environ['AUTO_DOCSTRING_DESCRIPTION_SEPARATOR'] = '\n        '

        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}):
                    {3!f}.

            Returns:
                {4:int!f}:
                    {5!f}.

            '''

        self.compare(expected_output, code)

    def test_description_separator_single(self):
        code = \
            '''
            def foo():
                {curs}
                return 8
            '''

        expected_output = '{1:int!f}: {2!f}.'
        self.compare(expected_output, code)

        os.environ['AUTO_DOCSTRING_DESCRIPTION_SEPARATOR'] = '\n        '

        expected_output = '{1:int!f}: {2!f}.'
        self.compare(expected_output, code)


class MarkupTestCase(ConfigCommonTestCase):
#     def test_third_party_prefix(self):
#         pass

#     def test_third_party_suffix(self):
#         pass

    def test_description_separator(self):
        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:list[tuple[str or float or int or bool]]!f}, optional): {5!f}.

            Returns:
                {6:int or bool!f}: {7!f}.

            '''

        self.compare(expected_output, self.simple_code)

        os.environ['AUTO_DOCSTRING_OPTION_SEPARATOR'] = ' |or| '

        new_tags_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:list[tuple[str |or| float |or| int |or| bool]]!f}, optional): {5!f}.

            Returns:
                {6:int |or| bool!f}: {7!f}.

            '''

        self.compare(new_tags_output, self.simple_code)

    def test_iter_tags(self):
        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:list[tuple[str or float or int or bool]]!f}, optional): {5!f}.

            Returns:
                {6:int or bool!f}: {7!f}.

            '''

        self.compare(expected_output, self.simple_code)

        os.environ['AUTO_DOCSTRING_CONTAINER_PREFIX'] = ' of '
        os.environ['AUTO_DOCSTRING_CONTAINER_SUFFIX'] = ''

        new_tags_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4:list of tuple of str or float or int or bool!f}, optional): {5!f}.

            Returns:
                {6:int or bool!f}: {7!f}.

            '''

        self.compare(new_tags_output, self.simple_code)
