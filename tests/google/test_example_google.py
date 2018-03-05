#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import unittest
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from auto_docstring import docstring_builder_two as docstring_builder

# IMPORT LOCAL LIBRARIES
from .. import common


class AdvancedTestCase(common.CommonTestCase):
    def compare(self, code, expected_output):
        code = textwrap.dedent(code)
        row, _ = common.get_position('{curs}', code.split('\n'))
        code.format(curs='')

        expected_output = textwrap.dedent(expected_output)
        generated_docstring = docstring_builder.create_ultisnips_docstring(code, row=row, style='google')

        self.assertEqual(expected_output, generated_docstring)

    def test_function_0001(self):
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

        self.compare(code, expected_output)

    def test_list_comp(self):
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
        self.compare(code, expected_output)

#     # def test_build_docstring_0002_nested_function_parent(self):
#     #     some_function = \
#     #         """\
#     #         def delete_ui_if_exists(*uis):
#     #             {curs}
#     #             def actual_decorator(func):
#     #                 '''The actual decorated function that will be passed.'''
#     #                 def wrapped_func(*args):
#     #                     '''Delete UIs before running the given function.

#     #                     Args:
#     #                         *args (list[str]): The args given by the original function.

#     #                     '''
#     #                     for ui in uis:
#     #                         try:
#     #                             pm.deleteUI(ui)
#     #                         except RuntimeError:
#     #                             pass

#     #                     return func(*args)
#     #                 return wrapped_func
#     #             return actual_decorator
#     #         """
#     #     expected_output = \
#     #         '''\
#     #         {1}.

#     #         Args:
#     #             *uis ({2}): {3}.

#     #         Returns:
#     #             actual_decorator: {4}.

#     #         '''
#     #     self.compare_docstring_with_output(input_text=some_function,
#     #                                        expected_output=expected_output)

#     def test_nested_function_parent(self):
#         code = \
#             """
#             def which(program):
#                 {curs}
#                 pathExt = ['']
#                 extList = None

#                 if sys.platform == 'win32':
#                     extList = [ext.lower() for ext in os.environ['PATHEXT'].split(';')]

#                 def is_exe(fpath):
#                     '''Checks if the filepath points to an executable file.

#                     Args:
#                         fpath (str): The full filepath

#                     Returns:
#                         bool: Whether or not the function is executable

#                     '''
#                     exe = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
#                     # search for executable under windows
#                     if not exe:
#                         if extList:
#                             for ext in extList:
#                                 exePath = '%s%s' % (fpath, ext) if os.path.isfile(exePath) and os.access(exePath, os.X_OK):
#                                     pathExt[0] = ext
#                                     return True
#                             return False
#                     return exe

#                 fpath, fname = os.path.split(program)

#                 if fpath:
#                     if is_exe(program):
#                         return '%s%s' % (program, pathExt[0])
#                 else:
#                     for path in os.environ['PATH'].split(os.pathsep):
#                         path = path.strip('"')
#                         exe_file = os.path.join(path, program)
#                         if is_exe(exe_file):
#                             return '%s%s' % (exe_file, pathExt[0])
#                 return ''
#             """

#         expected_output = \
#             '''\
#             {1}.

#             Args:
#                 program ({2}): {3}.

#             Returns:
#                 str: {4}.

#             '''
#         self.compare(code, expected_output)

    def test_nested_function(self):
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
        self.compare(code, expected_output)

    def test_complex_type_0001(self):
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

        self.compare(code, expected_output)

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

        self.compare(code, expected_output)
