#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A set of unittests for docstrings that raised exceptions.

These tests are presented in no particular order.

'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring import docstring_builder

# IMPORT LOCAL LIBRARIES
from .. import common


class AdvancedTestCase(common.CommonTestCase):

    '''A series of unittests for docstrings that required bugfixes.'''

    def compare(self, expected_output, code):
        '''Create `code` docstring and test it against `expected_output`.

        Args:
            expected_output (str): The docstring that should be built.
            code (str): The code that is used to create a docstring.

        '''
        code = textwrap.dedent(code)
        try:
            code = self._make_code(code)
        except TypeError:
            # If no %s was in the string, ignore it
            pass

        row, _ = common.get_position('{curs}', code.split('\n'))
        code = code.format(curs='')

        expected_output = textwrap.dedent(expected_output)
        generated_docstring = docstring_builder.create_ultisnips_docstring(
            code, row=row, style='google')

        # for index, (char1, char2) in enumerate(zip(expected_output, generated_docstring)):
        #     if char1 != char2:
        #         raise ValueError(expected_output[:index])
        #         raise ValueError(('asdfsfd', index, char1, char2))

        self.assertEqual(expected_output, generated_docstring)

    def test_function_0001(self):
        '''Create a correct docstring for a function with a nested function.'''
        code = \
            """
            def get_max_index(combo, idfun=None):
                {curs}
                if idfun is None:
                    def _idfun(text):
                        '''Default function that assumes that text is able to be an int.'''
                        return int(text)

                    idfun = _idfun

                highest_value = None
                index = -1
                for index in six.moves.range(combo.count()):
                    text = combo.itemText(index)
                    compare_object = idfun(text)
                    if highest_value is None or compare_object > idfun(highest_value):
                        highest_value = text
                        index = index

                return index
            """

        expected_output = \
            '''\
            $1.

            Args:
                combo ($2): $3.
                idfun (${4:NoneType}, optional): $5.

            Returns:
                ${6:int}: $7.

            '''

        self.compare(expected_output, code)

    def test_list_assignment(self):
        '''Create a docstring for a variable-list.'''
        code = \
            '''\
            import re

            def dirgrep(obj, keyPhrase='', case=True, stdout=True):
                {curs}
                flags = 0

                if case:
                    flags = re.IGNORECASE

                output = []
                for x in dir(obj):
                    if re.search(keyPhrase, x, flags=flags):
                        output.append(x)

                if stdout:
                    for x in output:
                        print x
                return output
            '''

        expected_output = \
            '''\
            $1.

            Args:
                obj ($2): $3.
                keyPhrase (${4:str}, optional): $5.
                case (${6:bool}, optional): $7.
                stdout (${8:bool}, optional): $9.

            Returns:
                ${10:list}: $11.

            '''
        self.compare(expected_output, code)

    def test_nested_function_parent_001(self):
        '''Create a docstring for the outter function of a wrapper function.'''
        code = \
            """\
            def delete_ui_if_exists(*uis):
                {curs}
                def actual_decorator(func):
                    '''The actual decorated function that will be passed.'''
                    def wrapped_func(*args):
                        '''Delete UIs before running the given function.

                        Args:
                            *args (list[str]): The args given by the original function.

                        '''
                        for ui in uis:
                            try:
                                pm.deleteUI(ui)
                            except RuntimeError:
                                pass

                        return func(*args)
                    return wrapped_func
                return actual_decorator
            """

        expected_output = \
            '''\
            $1.

            Args:
                *uis (${2:tuple}, optional): $3.

            Returns:
                ${4:actual_decorator}: $5.

            '''

        self.compare(expected_output, code)

    def test_nested_function_parent_002(self):
        '''Create a docstring for the outter function of a wrapper function.'''
        code = \
            """
            import os

            def which(program):
                {curs}
                pathExt = ['']
                extList = None

                if sys.platform == 'win32':
                    extList = [ext.lower() for ext in os.environ['PATHEXT'].split(';')]

                def is_exe(fpath):
                    exe = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
                    # search for executable under windows
                    if not exe:
                        if extList:
                            for ext in extList:
                                exePath = '%s%s' % (fpath, ext)
                                if os.path.isfile(exePath) and os.access(exePath, os.X_OK):
                                    pathExt[0] = ext
                                    return True
                            return False
                    return exe

                fpath, fname = os.path.split(program)

                if fpath:
                    if is_exe(program):
                        return '%s%s' % (program, pathExt[0])
                else:
                    for path in os.environ['PATH'].split(os.pathsep):
                        path = path.strip('"')
                        exe_file = os.path.join(path, program)
                        if is_exe(exe_file):
                            return '%s%s' % (exe_file, pathExt[0])
                return ''
            """

        expected_output = \
            '''\
            $1.

            Args:
                program ($2): $3.

            Returns:
                ${4:str}: $5.

            '''
        self.compare(expected_output, code)

    def test_nested_function(self):
        '''Create a docstring for the inner function of a wrapper function.'''
        code = \
            """
            import os

            def which(program):
                pathExt = ['']
                extList = None

                if sys.platform == 'win32':
                    extList = [ext.lower() for ext in os.environ['PATHEXT'].split(';')]

                def is_exe(fpath):
                    {curs}
                    exe = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
                    # search for executable under windows
                    if not exe:
                        if extList:
                            for ext in extList:
                                exePath = '%s%s' % (fpath, ext)
                                if os.path.isfile(exePath) and os.access(exePath, os.X_OK):
                                    pathExt[0] = ext
                                    return True
                            return False
                    return exe

                fpath, fname = os.path.split(program)

                if fpath:
                    if is_exe(program):
                        return '%s%s' % (program, pathExt[0])
                else:
                    for path in os.environ['PATH'].split(os.pathsep):
                        path = path.strip('"')
                        exe_file = os.path.join(path, program)
                        if is_exe(exe_file):
                            return '%s%s' % (exe_file, pathExt[0])
                return ''
            """

        expected_output = \
            '''\
            $1.

            Args:
                fpath ($2): $3.

            Returns:
                ${4:bool}: $5.

            '''
        self.compare(expected_output, code)

    def test_complex_type_0001(self):
        '''Check that a known default arg still returns the correct type.'''
        code = \
            '''\
            def get_clean_comma_sep_text(text, sep=', '):
                {curs}
                text = sep.join(
                    [text_.strip() for text_ in text.split(',') if text_.strip()])
                text = text.rstrip(',')
                return text
            '''

        expected_output = \
            '''\
            $1.

            Args:
                text ($2): $3.
                sep (${4:str}, optional): $5.

            Returns:
                ${6:str}: $7.

            '''

        self.compare(expected_output, code)

    def test_multi_instancemethod(self):
        '''Build docstrings for functions with more than one positional arg.'''
        code = \
            '''\
            class AnotherClass(object):
                def some_another_function(self, some_arg, another_arg):
                    {curs}
                    pass
            '''

        expected_output = \
            '''\
            $1.

            Args:
                some_arg ($2): $3.
                another_arg ($4): $5.

            '''

        self.compare(expected_output, code)

    def test_002(self):
        '''Make sure that the contents of a raised exception does not error.

        There was originally an issue where any string ending in "}" would break
        the parser whenever it became time to convert it into numbered strings.

        '''
        # Test that a message that starts with {, another that ends in }, and
        # one more that does both
        #
        code = \
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
            '''

        expected_output = \
            '''\
            $1.

            Args:
                arg1 ($2): $3.
                arg2 ($4): $5.
                thing (${6:tuple[tuple[str]]}, optional): $7.

            Raises:
                ValueError: ${8:asdfsd}.
                TypeError: ${10:${9:ffff}bar}.
                RuntimeError: ${12:${11:zzzz}}.
                NotImplementedError: ${14:bar${13:tttt}}.

            Returns:
                ${15:list[str]}: $16.

            '''

        self.compare(expected_output, code)
