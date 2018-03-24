#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from .. import common


class SphinxTestCase(common.CommonTestCase):
    def compare(self, expected_output, code):
        super(SphinxTestCase, self).compare(expected_output, code=code, style='sphinx')


class FunctionTestCase(SphinxTestCase):
    def test_no_arg(self):
        code = \
            '''
            def foo():
                {curs}
                pass
            '''

        expected_output = '{1!f}.'

        self.compare(expected_output, code)

    # def test_one_arg(self):
    #     code = \
    #         '''
    #         def foo(arg1):
    #             {curs}
    #             pass
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Parameters
    #         ----------
    #         :param arg1: {2!f}.
    #         :type arg1: {3!f}.

    #         '''

    #     self.compare(expected_output, code)

    # def test_multiple_args(self):
    #     code = \
    #         '''
    #         def foo(arg1, arg2):
    #             {curs}
    #             pass
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         :param arg1: {2!f}.
    #         :param arg2: {3!f}.
    #         :type arg1: {4!f}.
    #         :type arg2: {5!f}.

    #         '''

    #     self.compare(expected_output, code)

    # def test_default_args(self):
    #     code = \
    #         '''
    #         def foo(arg1, arg2=None):
    #             {curs}
    #             pass
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         :param arg1: {2!f}.
    #         :param arg2: {3!f}.
    #         :type arg1: {4!f}.
    #         :type arg2: {5:NoneType!f}.

    #         '''

    #     self.compare(expected_output, code)

    # def test_nested_args(self):
    #     code = \
    #         '''
    #         def foo(arg1, arg2=('asfdsdf', ['asfad'])):
    #             {curs}
    #             pass
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         :param arg1: {2!f}.
    #         :param arg2: {3!f}.
    #         :type arg1: {4!f}.
    #         :type arg2: {5:tuple[str or list[str]]!f}.

    #         '''

    #     self.compare(expected_output, code)


# class ReturnTestCase(SphinxTestCase):
    # def test_simple(self):
    #     code = \
    #         '''
    #         def foo(arg1, arg2):
    #             {curs}
    #             return 8
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         :param arg1: {2!f}.
    #         :param arg2: {3!f}.
    #         :type arg1: {4!f}.
    #         :type arg2: {5!f}.

    #         :return: {6!f}.
    #         :rtype: {7:int!f}.

    #         '''

    #     self.compare(expected_output, code)

    # def test_nested(self):
    #     code = \
    #         '''
    #         def foo(arg1, arg2):
    #             {curs}
    #             return ('asdfasd', ['ttt', 9])
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         :param arg1: {2!f}.
    #         :param arg2: {3!f}.
    #         :type arg1: {4!f}.
    #         :type arg2: {5!f}.

    #         :return: {6!f}.
    #         :rtype: {7:tuple[str or list[str or int]]!f}.

    #         '''

    #     self.compare(expected_output, code)
