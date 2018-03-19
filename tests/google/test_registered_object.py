#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests for "registered" objects.

auto_docstring type inspection is fairly good a picking up object types but,
when it fails, sometimes it is good to just directly specify the return type.

'''

# IMPORT STANDARD LIBRARIES
import os

# IMPORT AUTO-DOCSTRING LIBRARIES
from auto_docstring.blocks.google import common_block
import auto_docstring

# IMPORT LOCAL LIBRARIES
from .. import common


class BasicTestCase(common.CommonTestCase):

    '''Test simple registered functions, methods, and other objects.'''

    def test_unknown_module_function(self):
        '''Return the name of a function whose return types are uninferable.'''
        code = \
            '''
            import textwrap

            def get_default_indent():
                {curs}
                return textwrap.dedent('asfasdfaf')
            '''

        expected_output = '{1:<textwrap.dedent>!f}: {2!f}.'

        self.compare(expected_output, code)

    # TODO : Finish this one
    def test_registered_method(self):
        '''Register an explicit method's return type(s).'''
        code = \
            '''
            def get_default_indent():
                {curs}
                return 'asdffsd'.format('thing')
            '''

        auto_docstring.register(obj='str.format', returns='str')

        expected_output = '{1:str!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_registered_module_function(self):
        '''Register an explicit function's return type(s).'''
        import textwrap

        code = \
            '''
            import textwrap

            def get_default_indent():
                {curs}
                return textwrap.dedent('asfasdfaf')
            '''

        auto_docstring.register(obj=textwrap.dedent, returns='str')

        expected_output = '{1:str!f}: {2!f}.'

        self.compare(expected_output, code)


class ParseTestCase(common.CommonTestCase):

    '''A series of unittests for registered objects with dynamic return types.'''

    def test_getenv_001(self):
        '''Parse the return types of a function.'''
        def get_getenv_return_types(obj):
            from auto_docstring.blocks.google import common_block
            all_types = []
            for arg in obj.args:
                all_types.append(common_block.process_types(arg))
            return common_block.make_items_text(all_types)

        auto_docstring.register(obj=os.getenv, returns=get_getenv_return_types)

        code = \
            '''
            import textwrap

            def get_default_indent():
                {curs}
                return os.getenv('something', False)
            '''

        expected_output = '{1:str or bool!f}: {2!f}.'

        self.compare(expected_output, code)

    def test_getenv_002(self):
        def get_getenv_return_types(obj):
            from auto_docstring.blocks.google import common_block
            all_types = []
            for arg in obj.args:
                all_types.append(common_block.process_types(arg))
            return common_block.make_items_text(all_types)

        auto_docstring.register(obj=os.getenv, returns=get_getenv_return_types)

        code = \
            '''
            import textwrap

            def bar(arg1):
                if arg1:
                    return 10.8
                return False

            def get_default_indent():
                {curs}
                return os.getenv('something', bar())
            '''

        auto_docstring.register(obj=os.getenv, returns=get_getenv_return_types)

        expected_output = '{1:str or float or bool!f}: {2!f}.'

        self.compare(expected_output, code)
