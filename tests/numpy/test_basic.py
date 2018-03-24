#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from .. import common


class NumpyTestCase(common.CommonTestCase):
    def compare(self, expected_output, code):
        super(NumpyTestCase, self).compare(expected_output, code=code, style='numpy')


class FunctionTestCase(NumpyTestCase):
    def test_no_arg(self):
        code = \
            '''
            def foo():
                {curs}
                pass
            '''

        expected_output = \
            '''{1!f}.

            '''

        self.compare(expected_output, code)

    def test_one_arg(self):
        code = \
            '''
            def foo(arg1):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.

            '''

        self.compare(expected_output, code)

    def test_multiple_args(self):
        code = \
            '''
            def foo(arg1, arg2):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4!f}
                {5!f}.

            '''

        self.compare(expected_output, code)

    def test_default_args(self):
        code = \
            '''
            def foo(arg1, arg2=None):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4:NoneType!f}
                {5!f}.

            '''

        self.compare(expected_output, code)

    def test_nested_args(self):
        code = \
            '''
            def foo(arg1, arg2=('asfdsdf', ['asfad'])):
                {curs}
                pass
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4:tuple[str or list[str]]!f}
                {5!f}.

            '''

        self.compare(expected_output, code)


class ReturnTestCase(NumpyTestCase):
    def test_simple(self):
        code = \
            '''
            def foo(arg1, arg2):
                {curs}
                return 8
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4!f}
                {5!f}.

            Returns
            -------
            {6:int!f}
                {7!f}.

            '''

        self.compare(expected_output, code)

    def test_nested(self):
        code = \
            '''
            def foo(arg1, arg2):
                {curs}
                return ('asdfasd', ['ttt', 9])
            '''

        expected_output = \
            '''\
            {1!f}.

            Parameters
            ----------
            arg1 : {2!f}
                {3!f}.
            arg2 : {4!f}
                {5!f}.

            Returns
            -------
            {6:tuple[str or list[str or int]]!f}
                {7!f}.

            '''

        self.compare(expected_output, code)


class RaisesTestCase(NumpyTestCase):
    def test_basic(self):
        code = \
            '''
            def foo():
                {curs}
                raise ValueError('Some message.')
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises
            ------
            ValueError
                {2:Some message!f}.

            '''

        self.compare(expected_output, code)
