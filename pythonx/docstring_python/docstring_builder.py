#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module that holds classes and functions to draw docstrings.'''

# IMPORT STANDARD LIBRARIES
import os
import re

# IMPORT LOCAL LIBRARIES
# TODO : Make this relative
from core.formatting import str_format


class PassThroughDict(object):

    '''.'''

    def __init__(self):
        '''.'''
        super(PassThroughDict, self).__init__()

    def __getitem__(self, key):
        return key


class DocstringPython(object):

    '''Responsible for asking what to draw and drawing Python docstrings.'''

    valid_display_orders = ['Arg', 'Args', 'Attribute', 'Attributes', 'Raise',
                            'Raises', 'Return', 'Returns', 'Yield', 'Yields']

    def __init__(self, parser, style):
        '''Store the information needed to create a docstring.

        Args:
            parser (ParserPython): The object to query docstring data from.
            style: The style to draw the docstring in.

        '''
        super(DocstringPython, self).__init__()
        self.parser = parser
        self.style = style

    @classmethod
    def get_block_order(cls):
        '''list[str]: The order of each display block.'''
        display_order = os.getenv('DOCSTRING_DISPLAY_ORDER')
        if display_order is None:
            # fallback to a default order, in case none was found
            return cls.valid_display_orders

        display_orders = []
        for display in display_order.split('\n'):
            display = display.strip()
            if display:
                display_orders.append(display)

        invalid_displays = set(display_orders) - cls.valid_display_orders
        if invalid_displays:
            return ValueError('Got bad display types: "{disp}". Options were, '
                              '"{opt}".'.format(disp=sorted(invalid_displays),
                                                opt=cls.valid_display_orders))
        return display_orders

    def create_docstring(self):
        '''str: Draw an automatic Python docstring.'''
        context = self.parser.get_context()
        row_info = self.parser.get_info(self.parser.get_row_type(),
                                        node_type=context)
        blocks = row_info.get('blocks')

        # Build blocks that will represent our docstrings
        final_blocks = []
        for block in [block for block in self.get_block_order()
                      if block in blocks]:
            block_object = self.style.get_block(block)
            if block_object is None:
                continue
            block_object = block_object(block)

            for arg_info in blocks.get(block, []):
                block_object.add_block_object_raw(arg_info)
            final_blocks.append(block_object)

        # Display each block's docstring information
        output_str = '{1}.\n\n'
        offset_value = 1
        number_formatter = str_format.NumberifyWordFormatter()
        for block in final_blocks:
            if block.is_empty():
                continue

            block_str = block.draw('formatted')
            is_last_element = final_blocks.index(block) == len(final_blocks) - 1
            if not is_last_element:
                block_str += '\n\n'

            offset_value = get_offset_value(output_str)

            # Add numbers wherever needed
            block_str = number_formatter.format(block_str, dict())

            formatter = str_format.OffsetFormatter(offset=offset_value + 1)
            block_str = formatter.format(block_str, PassThroughDict())

            output_str += block_str

        formatter = str_format.NumberifyFormatter()
        output_str = formatter.format(output_str)

        return output_str


def get_offset_value(input_str):
    match = re.search('{(\d+)}', input_str)
    if not match:
        return 0

    if match:
        return max((int(num) for num in match.groups()))



if __name__ == '__main__':
    print(__doc__)

