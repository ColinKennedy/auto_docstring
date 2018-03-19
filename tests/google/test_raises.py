#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A collection of unittests for the "Raises" docstring block.'''

# IMPORT LOCAL LIBRARIES
from .. import common


class GenericTestCase(common.CommonTestCase):

    '''Test a number of very simple exception cases.'''

    def test_002(self):
        '''Make sure that the contents of a raised exception does not error.

        There was originally an issue where any string ending in "}" would break
        the parser whenever it became time to convert it into numbered strings.

        '''
        # Test that a message that starts with {, another that ends in }, and
        # one more that does both
        #
        code = self._make_code(
            '''
            def foo(arg1, arg2, thing=(('asfd', 'asdfsfd'), )):
                %s
                message = 'asdfsd'
                if arg2:
                    raise ValueError(message)

                if thing[0]:
                    raise TypeError('{ffff}bar'.format(ffff=9123))

                if thing[1]:
                    raise RuntimeError('{zzzz}'.format(zzzz=9123))

                if arg1:
                    raise NotImplementedError('bar{tttt}'.format(tttt=9123))

                return ['asdfsdf', 'adsfafds']
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                arg1 ({2!f}): {3!f}.
                arg2 ({4!f}): {5!f}.
                thing ({6:tuple[tuple[str]]!f}, optional): {7!f}.

            Raises:
                ValueError: {8:asdfsd!f}.
                TypeError: {10:{9:ffff!f}bar!f}.
                RuntimeError: {12:{11:zzzz!f}!f}.
                NotImplementedError: {14:bar{13:tttt!f}!f}.

            Returns:
                {15:list[str]!f}: {16!f}.

            '''

        self.compare(expected_output, code)

    def test_no_message(self):
        '''Raise an exception but do not call it.'''
        code = \
            '''
            def foo():
                {curs}
                raise ValueError
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {2!f}.

            '''

        self.compare(expected_output, code)

    def test_blank_message(self):
        '''Raise an exception and call it, with no message.'''
        code = \
            '''
            def foo():
                {curs}
                raise ValueError()
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {2!f}.

            '''

        self.compare(expected_output, code)

    def test_raises(self):
        '''Raise an exception that contains some message.'''
        code = \
            '''
            def foo(bar):
                {curs}
                raise ValueError('Info here.')

                if bar:
                    raise OSError('Info here.')
            '''

        expected_output = \
            '''\
            {1!f}.

            Args:
                bar ({2!f}): {3!f}.

            Raises:
                ValueError: {4:Info here!f}.
                OSError: {5:Info here!f}.

            '''

        self.compare(expected_output, code)

    def test_empty(self):
        '''Implicitly raise an exception.'''
        code = \
            '''
            def foo():
                {curs}
                try:
                    bar.fizz()
                except ValueError:
                    raise
            '''

        expected_output = '{1!f}.'

        self.compare(expected_output, code)

    def test_percent(self):
        '''Convert %d/%s/%r to inner tabstops.'''
        code = \
            '''
            def foo():
                {curs}
                raise ValueError('Something "%s" "%d" "%r" "%f" here')
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {6:Something "{2:!f}" "{3:!f}" "{4:!f}" "{5:!f}" here!f}.

            '''

        self.compare(expected_output, code)

    def test_drop_dot(self):
        '''Remove "." if it is in the docstring.'''
        code = \
            '''
            def foo():
                {curs}
                raise ValueError('Something here.')
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {2:Something here!f}.

             '''

        self.compare(expected_output, code)


class NameTestCase(common.CommonTestCase):

    '''Test different scenarios for Name objects.'''

    def test_variable_message(self):
        '''Test a message that is assigned as a variable.'''
        code = \
            '''
            def foo():
                {curs}
                message = 'example message'
                raise ValueError(message)
            '''

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {2:example message!f}.

            '''

        self.compare(expected_output, code)

    def test_variable_unformatted_message(self):
        '''Test an unformatted string and that {}s is added to it.'''
        code = self._make_code(
            '''
            def foo():
                %s
                message = 'example {bar} message'
                raise ValueError(message)
            ''')

        expected_output = \
            '''\
            {1!f}.

            Raises:
                ValueError: {3:example {2:bar!f} message!f}.

            '''

        self.compare(expected_output, code)

    # TODO : Come back to with one
    # def test_variable_formatted_message(self):
    #     code = self._make_code(
    #         '''
    #         def foo():
    #             %s
    #             message = 'example {bar} message'.format(bar=8)
    #             raise ValueError(message)
    #         ''')

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Raises:
    #             ValueError: {3:example {2:bar!f} message!f}.

    #         '''

    #     self.compare(expected_output, code)


class CallTestCase(common.CommonTestCase):

    '''Test different exceptions that use callable objects.'''

    def test_001(self):
        '''Test str.format and make sure it returns strings correctly.'''
        code = self._make_code(
            '''
            def add_docstring():
                %s
                raise NotImplementedError('Need to write this')
                raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
                                 ''.format(mode=mode, options=options))
            ''')

        expected_output = \
            '''\
            {1!f}.

            Raises:
                NotImplementedError: {2:Need to write this!f}.
                ValueError: {5:Mode: "{3:mode!f}" is unsupported. Options were, "{4:options!f}"!f}.

            '''

        self.compare(expected_output, code)

    def test_002(self):
        '''Test str.format and make sure it returns strings correctly.'''
        code = self._make_code(
            '''
            def add_docstring(code, row, style='', mode='replace'):
                %s
                code = list(code)
                docstring = create_docstring(code=code, row=row, style=style)

                if mode == 'replace':
                    raise NotImplementedError('Need to write this')
                    # code[row:] = docstring
                elif mode == 'insert':
                    code.insert(row, docstring)
                else:
                    options = ('replace', 'insert')
                    raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
                                     ''.format(mode=mode, options=options))

                return code
            ''')

        expected_output = \
            '''\
            {1!f}.

            Args:
                code ({2!f}): {3!f}.
                row ({4!f}): {5!f}.
                style ({6:str!f}, optional): {7!f}.
                mode ({8:str!f}, optional): {9!f}.

            Raises:
                NotImplementedError: {10:Need to write this!f}.
                ValueError: {13:Mode: "{11:mode!f}" is unsupported. Options were, "{12:options!f}"!f}.

            Returns:
                {14:list!f}: {15!f}.

            '''

        self.compare(expected_output, code)

    # TODO : Finish these tests, later
    # def test_attribute_raise(self):
    #     code = \
    #         '''
    #         class Foo(object):

    #             bar = 'ttt'


    #         def foo():
    #             {curs}
    #             raise ValueError(Foo.bar)
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Raises:
    #             ValueError: {2:ttt!f}.

    #         '''

    #     self.compare(expected_output, code)

    # def test_call_raise(self):
    #     code = \
    #         '''
    #         def message():
    #             return 'asfdasdf'


    #         def foo():
    #             {curs}
    #             raise ValueError(message())
    #         '''

    #     expected_output = \
    #         '''\
    #         {1!f}.

    #         Raises:
    #             ValueError: {2:asfdasdf!f}.

    #         '''

    #     self.compare(expected_output, code)
