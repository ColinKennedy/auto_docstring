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
            {
                'name': arg_name,
                'arg_type': arg_type,
                'message': text
            })

    def draw(self, method):
        '''Create a string representation of this block.

        Args:
            method (str): The way that the text will be drawn.
                          For example, 'formatted' will wrap all variable data
                          into '{}'s, so that Python can continue to format it.

        Returns:
            str: The docstring block, as text.

        '''
        if method != 'formatted':
            raise NotImplementedError('Only the "formatted" method is allowed.')

        output_str = str(self.label) + ':\n'
        for info_dict in self.block_info:
            output_str += '{indent}{name}'.format(indent='    ',
                                                  name=info_dict.get('name'))
            info_type = self.get_type(info_dict)
            output_str += info_type

            output_str += ': '

            info_message = info_dict.get('message', '')
            output_str += '{' + info_message + '}.'

            is_last = self.block_info.index(info_dict) == \
                len(self.block_info) - 1

            if not is_last:
                output_str += '\n'

        return output_str

    def get_type(self, info):
            block_type = info.get('type', '')
            if block_type:
                return ' ({' + str(block_type) + '}, optional)'
            return ' ({})'


class MultiNoTypeBlock(MultiTypeBlock):
    def __init__(self, label):
        super(MultiNoTypeBlock, self).__init__(label=label)

    def get_type(self, info):
        return ''


class InlineTypeBlock(MultiTypeBlock):
    def __init__(self, label):
        super(InlineTypeBlock, self).__init__(label=label)

    def draw(self, method):
        super(InlineTypeBlock, self).draw(method=method)
        output_str = str(self.label) + ':\n'
        types_ = [block.get('type') for block in self.block_info]

        item_types = []
        for type_ in types_:
            if type_ not in item_types:
                item_types.append(type_)

        try:
            item_types[0] = '    ' + item_types[0]
        except IndexError:
            # This shouldn't ever happen because, ideally, if this method has
            # information in its block, it should have some idea of its type
            #
            item_types = []

        if item_types:
            output_str += ' or '.join(item_types) + ':'
            output_str += ' {}.'
        else:
            output_str += '    '

        return output_str


class GoogleStylePython(object):

    block_types = \
        {
            'Args': MultiTypeBlock,
            'Attributes': MultiTypeBlock,
            'Raises': MultiNoTypeBlock,
            'Returns': InlineTypeBlock,
            'Yields': InlineTypeBlock,
        }

    def __init__(self):
        '''Initialize the object and do nothing else.'''
        super(GoogleStylePython, self).__init__()

    @classmethod
    def get_block(cls, name):
        return cls.block_types.get(name)


if __name__ == '__main__':
    print(__doc__)

