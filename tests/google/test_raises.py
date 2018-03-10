#!/usr/bin/env python
#

# IMPORT LOCAL LIBRARIES
from .. import common


class NameTestCase(common.CommonTestCase):
    def test_variable_message(self):
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
    def test_001(self):
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
                ValueError: {5:Mode: "{3:mode!f}" is unsupported. Options were, "{4:options!f}".!f}.

            '''

        self.compare(expected_output, code)

    def test_002(self):
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
                ValueError: {13:Mode: "{11:mode!f}" is unsupported. Options were, "{12:options!f}".!f}.

            Returns:
                {14:list!f}: {15!f}.

            '''

        self.compare(expected_output, code)
