#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''All tests for building docstrings, in a variety of code scenarios.'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest
import abc

# IMPORT THIRD-PARTY LIBRARIES
from docstring_python import class_read
import common


class FunctionTestAbstractInterface(object):

    '''Make sure that all function tests support the minimum-required tests.'''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def test_build_docstring_no_args(self):
        '''Make a docstring that is just a summary line.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_one_arg(self):
        '''Make a function docstring that has one positional arg.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_multi_args(self):
        '''Build docstrings for functions with more than one positional arg.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg(self):
        '''Create a docstring that has default arg info.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg_custom(self):
        '''Build a docstring that has a default arg that is not built in.'''
        pass

    @abc.abstractmethod
    def test_build_docstring_default_arg_statement(self):
        '''Make a function docstring that prefers a built-in statement.

        For example, if the default arg is a bool or NoneType, the text that
        the docstring changes from 'Default: X' to 'Default is X'.

        '''
        pass

    @abc.abstractmethod
    def test_build_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        pass

    @abc.abstractmethod
    def test_build_yield_docstring(self):
        '''.'''
        pass


class CommonFunctionTestCase(common.CommonTestCase):

    '''A simple unittest that has some brief helper methods.

    Keep test code short.

    '''

    def get_docstring(self, input_text):
        '''<docstring.PythonGoogleDocstring>: The docstring for this text.'''
        input_text = input_text.format(curs=self.cursor.pointer)
        input_text = textwrap.dedent(input_text)
        row, _ = self.cursor.get_position(input_text.split('\n'))

        return class_read.create_auto_docstring(
            code=input_text, row=row, language='python', style='google')

    def compare_docstring_with_output(self, input_text, expected_output):
        '''Compare the docstring that the input creates with the expected.

        Args:
            input_text (list[str]): The input text.
            expected_output (str): The output docstring that input_text
                                   should make.

        '''
        docs = self.get_docstring(input_text)
        expected_output = textwrap.dedent(expected_output)
        self.assertEqual(docs, expected_output)


class BuildFunctionDocstringTestCase(CommonFunctionTestCase, unittest.TestCase):

    '''Create docstrings for a napoleon-style function.'''

    # def test_build_docstring_no_args(self):
    #     '''Make a docstring that is just a summary line.'''
    #     pass

    def test_build_docstring_one_arg(self):
        '''Make a function docstring that has one positional arg.'''
        some_function = \
            '''\
            def some_function(some_arg):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_multi_args(self):
        '''Build docstrings for functions with more than one positional arg.'''
        some_function = \
            '''\
            def some_function(some_arg, another_arg):
                {curs}
                pass
            '''.format(curs=self.cursor.pointer)
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.
                another_arg ({4}): {5}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_default_arg(self):
        '''Create a docstring that has default arg info.'''
        some_function = \
            '''\
            def some_function(some_arg=8):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:int}, optional): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_arg_and_default_arg(self):
        '''Make a docstring that has one positional arg and an optional arg.'''
        some_function = \
            '''\
            def some_function(something, another=8):
                {curs}
                return True
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                something ({2}): {3}.
                another ({4:int}, optional): {5}.

            Returns:
                bool: {6}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_default_arg_custom(self):
        '''Build a docstring that has a default arg that is not built in.'''
        some_function = \
            '''\
            def some_function(collect=collections.OrderedDict()):
                {curs}
                pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                collect ({2:<collections.OrderedDict>}, optional): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    # def test_build_docstring_default_arg_statement(self):
    #     '''Make a function docstring that prefers a built-in statement.

    #     For example, if the default arg is a bool or NoneType, the format of
    #     the default text is 'Default is X'.

    #     '''
    #     pass

    def test_build_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        some_function = \
            '''\
            def some_function(some_arg=collections.OrderedDict()):
                {curs}
                return True
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_return_single_type(self):
        '''Build a docstring that has one return type but multiple returns.'''
        some_function = \
            '''\
            def some_function(some_arg=collections.OrderedDict()):
                {curs}
                if something:
                    return True
                return False

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        some_function = \
            '''\
            def some_function(some_arg=collections.OrderedDict()):
                {curs}
                if something:
                    return True
                return ''

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool or str: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_yield_docstring(self):
        '''Make a docstring to describe a function that has a yield value.'''
        some_function = \
            '''\
            def some_function(some_arg=collections.OrderedDict()):
                {curs}
                if something:
                    yield True
                yield []

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Yields:
                bool or list: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_nested_function_docstring(self):
        some_function = \
            '''\
            def an_outer_function(*args, **kwargs):
                def inner_function(some_arg=collections.OrderedDict()):
                    {curs}
                    if something:
                        yield True
                    yield []

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Yields:
                bool or list: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_nested_function_parent_function(self):
        some_function = \
            '''\
            def a_parent_wrapped_func(yyy='asfd'):
                {curs}
                def some_function(some_arg=collections.OrderedDict()):
                    if something:
                        yield True
                    yield []

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                yyy ({2:str}, optional): {3}.

            Yields:
                bool or list: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    # def test_build_return_docstring_implicit(self):
    #     '''Create a docstring where one or more bare return is used.'''
    #     pass

    # def test_build_yield_docstring_implicit(self):
    #     '''Create a docstring where one or more bare yield is used.'''
    #     pass

    # def test_build_docstring_multiline_args(self):
    #     '''Build a function docstring from a definition that is 2+ lines.'''
    #     pass


class BuildMethodDocstringTestCase(CommonFunctionTestCase, unittest.TestCase):

    '''A suite of docstring test cases for class instancemethods.'''

    def test_build_docstring_one_arg(self):
        '''Create a docstring for a method that takes only one arg.'''
        some_function = \
            '''\
            class SomeClass(object):
                def some_function(self, some_arg):
                    {curs}
                    pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_one_arg_0001(self):
        some_function = \
            """\
            class asdfsdf(object):

                '''.'''

                def __init__(self):
                    '''asdfsfdsfdsdfasfdsd.'''
                    super(asdfsdf, self).__init__()

                def some_method(self, something):
                    {curs}
                    return False
            """
        expected_output = \
            '''\
            {1}.

            Args:
                something ({2}): {3}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_one_arg_0002(self):
        some_function = \
r"""\
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MultiTypeBlock(object):

    '''A class that represents a section of a docstring.

    It contains methods to add information to its internal data as well as
    how to draw that information, as text.

    '''

    def __init__(self, label):
        '''Initialize block information, along with this object instance.'''
        super(MultiTypeBlock, self).__init__()
        self.label = label
        self.block_info = []

    def is_empty(self):
        return not self.block_info

    def add_block_object_raw(self, info):
        '''Add the information directly into the object instance's data.

        Args:
            info (dict[str: str]): The information to add in, directly.

        '''
        self.block_info.append(info)

    def add_block_object(self, arg_name='', arg_type='', text=''):
        '''Format the information and add it to this object instance.

        Args:
            arg_name (str): The name or label of this object.
            arg_type (str): The object type (example: 'str', 'bool').
            text (str): Any information to send along with this object.

        Raises:
            RuntimeError: If none of the optional args for this method were
                          given any values.

        '''
        if arg_name == '' and arg_type == '' and text == '':
            raise RuntimeError('Please give at least a name, type or message.')

        self.block_info.append(
            {{
                'name': arg_name,
                'arg_type': arg_type,
                'message': text
            }})

    def draw(self, method):
        '''Create a string representation of this block.

        Args:
            method (str): The way that the text will be drawn.
                          For example, 'formatted' will wrap all variable data
                          into '{{}}'s, so that Python can continue to format it.

        Returns:
            str: The docstring block, as text.

        '''
        if method != 'formatted':
            raise NotImplementedError('Only the "formatted" method is allowed.')

        output_str = str(self.label) + ':\n'
        for info_dict in self.block_info:
            output_str += '{{indent}}{{name}}'.format(indent='    ',
                                                  name=info_dict.get('name'))
            info_type = self.get_type(info_dict)
            output_str += info_type

            output_str += ': '

            info_message = info_dict.get('message', '')
            output_str += '{{' + info_message + '}}.'

            is_last = self.block_info.index(info_dict) == \
                len(self.block_info) - 1

            if not is_last:
                output_str += '\n'

        return output_str

    def get_type(self, info):
        block_type = info.get('type', '')
        if block_type:
            return ' ({{' + str(block_type) + '}}, optional)'
        return ' ({{}})'


class MultiNoTypeBlock(MultiTypeBlock):
    def __init__(self, labels):
        super(MultiNoTypeBlock, self).__init__(labels=labels)
        self.labels = labels
        self.block_info = []

    def get_type(self, info):
        {curs}
        return ''


class InlineTypeBlock(MultiTypeBlock):
    def __init__(self, label):
        super(InlineTypeBlock, self).__init__(label=label)

    def draw(self, method):
        super(InlineTypeBlock, self).draw(method=method)
        output_str = str(self.label) + ':\n'
        types_ = [block.get('type') for block in self.block_info]

        types = []
        for type_ in types_:
            if type_ not in types:
                types.append(type_)

        try:
            types[0] = '    ' + types[0]
        except IndexError:
            # This shouldn't ever happen because, ideally, if this method has
            # information in its block, it should have some idea of its type
            #
            types = []

        output_str += ' or '.join(types) + ':'
        output_str += ' {{}}.'

        return output_str


class GoogleStylePython(object):

    block_types = \
        {{
            'Args': MultiTypeBlock,
            'Attributes': MultiTypeBlock,
            'Raises': MultiNoTypeBlock,
            'Returns': InlineTypeBlock,
            'Yields': InlineTypeBlock,
        }}

    def __init__(self):
        '''Initialize the object and do nothing else.'''
        super(GoogleStylePython, self).__init__()

    @classmethod
    def get_block(cls, name):
        return cls.block_types.get(name)


if __name__ == '__main__':
    print(__doc__)

"""
        expected_output = \
            '''\
            {1}.

            Args:
                info ({2}): {3}.

            Returns:
                str: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_multi_args(self):
        '''Build docstrings for functions with more than one positional arg.'''
        some_function = \
            '''\
            class AnotherClass(object):
                def some_another_function(self, some_arg, another_arg):
                    {curs}
                    pass
            '''.format(curs=self.cursor.pointer)
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2}): {3}.
                another_arg ({4}): {5}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_default_arg(self):
        '''Create a docstring that has default arg info.'''
        some_function = \
            '''\
            class TaskClass(object):
                def some_function(self, some_arg=8):
                    {curs}
                    pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:int}, optional): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_docstring_default_arg_custom(self):
        '''Build a docstring that has a default arg that is not built in.'''
        some_function = \
            '''\
            class Torch(object):
                def some_function(self, some_arg=collections.OrderedDict()):
                    {curs}
                    pass
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        some_function = \
            '''\
            class Fountain(object):
                def some_function(self, some_arg=collections.OrderedDict()):
                    {curs}
                    return True
            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_return_single_type(self):
        '''Build a docstring that has one return type but multiple returns.'''
        some_function = \
            '''\
            class Process(object):
                def some_function(self, some_arg=collections.OrderedDict()):
                    {curs}
                    if something:
                        return True
                    return False

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_return_docstring(self):
        '''Make a docstring to describe a function that has a return value.'''
        some_function = \
            '''\
            class TipTop(object):
                def some_function(self, some_arg=collections.OrderedDict()):
                    {curs}
                    if something:
                        return True
                    return ''

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Returns:
                bool or str: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_build_multi_yield_docstring(self):
        '''Make a docstring to describe a function that has a yield value.'''
        some_function = \
            '''\
            class JazzyBoy(object):
                def some_function(self, some_arg=collections.OrderedDict()):
                    {curs}
                    if something:
                        yield True
                    yield []

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Yields:
                bool or list: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_nested_class_instancemethod(self):
        some_function = \
            '''\
            class InnerClass(object):
                class JazzyBoy(object):
                    def some_function(self, some_arg=collections.OrderedDict()):
                        {curs}
                        if something:
                            yield True
                        yield []

            '''
        expected_output = \
            '''\
            {1}.

            Args:
                some_arg ({2:<collections.OrderedDict>}, optional): {3}.

            Yields:
                bool or list: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    # def test_method_attribute(self):
    #     '''Add attribute(s) to a method if it is defined out of __init__.'''
    #     some_function = \
    #         '''\
    #         class JazzyBoy(object):
    #             def __init__(self):
    #                 super(JazzyBoy, self).__init__()

    #             def some_function(self):
    #                 {curs}
    #                 self.out_of_init_attribute = 'tt'

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Attributes:
    #             out_of_init_attribute ({2:str}): {3}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)

    # # def test_method_attribute_init(self):
    # #     '''Add any attribute defined to docstring if method is __init__.'''
    # #     # TODO : Write this test case
    # #     some_function = \
    # #         '''\
    # #         class JazzyBoy(object):
    # #             def __init__(self):
    # #                 super(JazzyBoy, self).__init__()
    # #                 {curs}
    # #                 self.tetsu = 'jin'
    # #                 self.founder = True

    # #         '''
    # #     expected_output = \
    # #         '''\
    # #         {1}.

    # #         Attributes:
    # #             tetsu ({str}): {2}
    # #             founder ({True}): {3}

    # #         '''
    # #     self.compare_docstring_with_output(input_text=some_function,
    # #                                        expected_output=expected_output)

    # def test_method_attribute_multi(self):
    #     '''Append a field for each attribute found.'''
    #     some_function = \
    #         '''\
    #         class JazzyBoy(object):
    #             def __init__(self):
    #                 super(JazzyBoy, self).__init__()

    #             def some_function(self):
    #                 {curs}
    #                 self.out_of_init_attribute = 'tt'
    #                 self.anotherthing = 8

    #         '''
    #     expected_output = \
    #         '''\
    #         {1}.

    #         Attributes:
    #             out_of_init_attribute ({str}): {2}.
    #             anotherthing ({int}): {4}.

    #         '''
    #     self.compare_docstring_with_output(input_text=some_function,
    #                                        expected_output=expected_output)


class FunctionDocstringPositionTestCase(CommonFunctionTestCase, unittest.TestCase):

    def setUp(self):
        super(FunctionDocstringPositionTestCase, self).setUp()
        self.functions = \
            '''
            def a_1st_function(something):
                {top}
                pass


            def a_2nd_function(second_function_arg, argzilla=119):
                {mid}
                if a_thing:
                    return ''
                return True


            def a_3rd_function(third_function_arg, top='right'):
                {bottom}
                yield 'both'
            '''

    def test_top_function_in_file(self):
        some_function = self.functions.format(top='{curs}', mid='', bottom='')
        expected_output = \
            '''\
            {1}.

            Args:
                something ({2}): {3}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_middle_function_in_file(self):
        some_function = self.functions.format(top='', mid='{curs}', bottom='')
        expected_output = \
            '''\
            {1}.

            Args:
                second_function_arg ({2}): {3}.
                argzilla ({4:int}, optional): {5}.

            Returns:
                str or bool: {6}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_end_function_in_file(self):
        some_function = self.functions.format(top='', mid='', bottom='{curs}')
        expected_output = \
            '''\
            {1}.

            Args:
                third_function_arg ({2}): {3}.
                top ({4:str}, optional): {5}.

            Yields:
                str: {6}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)



class DocstringRaiseTestCase(CommonFunctionTestCase, unittest.TestCase):
    def test_no_raise(self):
        some_function = \
            '''\
            def some_function():
                {curs}
                pass
            '''
        expected_output = \
            '''{1}.'''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_one_raise(self):
        some_function = \
            '''\
            def some_function():
                {curs}
                raise ValueError('TTTT')
            '''
        expected_output = \
            '''\
            {1}.

            Raises:
                ValueError: {2:TTTT}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_multi_raise(self):
        some_function = \
            '''\
            def some_function():
                {curs}
                raise ValueError('TTTT')
                raise TypeError('ZZZ')
            '''
        expected_output = \
            '''\
            {1}.

            Raises:
                ValueError: {2:TTTT}.
                TypeError: {3:ZZZ}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)

    def test_multi_raise_and_return(self):
        some_function = \
            '''\
            def some_function():
                {curs}
                if some_condition:
                    raise ValueError('TTTT')
                    raise TypeError('ZZZ')

                return True
            '''
        expected_output = \
            '''\
            {1}.

            Raises:
                ValueError: {2:TTTT}.
                TypeError: {3:ZZZ}.

            Returns:
                bool: {4}.

            '''
        self.compare_docstring_with_output(input_text=some_function,
                                           expected_output=expected_output)


# class BuildClassDocstringTestCase(unittest.TestCase):

    # '''A suite of tests for class-level docstrings.'''

    # # docstring summary line
    # # Attribute
    # # Attributes

    # pass


# class BuildModuleDocstringTestCase(unittest.TestCase):

    # '''A suite of tests for module-level docstrings.'''

    # # Summary line
    # # Attribute
    # # Attributes
    # # Summary lines of classes and docstrings?

    # pass


# if __name__ == '__main__':
    # print(__doc__)


