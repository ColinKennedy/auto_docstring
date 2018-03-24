#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import os

# IMPORT LOCAL LIBRARIES
from . import common


class StyleEnvVarTestCase(common.CommonTestCase):
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
        super(StyleEnvVarTestCase, self).compare(expected_output, code, style='')

    def setUp(self):
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
        super(StyleEnvVarTestCase, self).setUp()

    def test_google(self):
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

    def test_sphinx(self):
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
