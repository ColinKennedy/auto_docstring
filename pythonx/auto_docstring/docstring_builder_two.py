#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import astroid

# IMPORT LOCAL LIBRARIES
from . import visit
from . import common
from . import numberify


def create_docstring(code, row, style=''):
    if not style:
        style = common.OPTIONS.get('style')

    # Parse the code
    node = astroid.parse(code)
    full_info = visit.get_info(node)

    node_that_needs_a_docstring = visit.get_closest_docstring_node(row, full_info)

    # Find the node's group and then get its info
    group = full_info['nodes'][node_that_needs_a_docstring]
    docstring_info = full_info[group][node_that_needs_a_docstring]

    # draw the docstring!
    style_object = common.create_code_style(style, full_info)
    initial_docstring = '\n'.join(style_object.draw(docstring_info))

    # Now the most important part, we need to convert the docstring that was
    # generated into a numbered-format string
    # Example:
    #     '''{}.
    #
    #     {name}
    #
    #     Args:
    #         foo ({}): {name}.
    #
    #     '''
    #
    #     must be change into ...
    #
    #     '''{1}.
    #
    #     {2|name}
    #
    #     Args:
    #         foo ({3}): {2|name}.
    #
    #     '''
    #
    formatter = numberify.NumberifyWordFormatter()
    numberized_docstring = formatter.format(initial_docstring)
    return numberized_docstring


def add_docstring(code, row, style='', mode='replace'):
    code = list(code)
    docstring = create_docstring(code=code, row=row, style=style)

    if mode == 'replace':
        raise NotImplementedError('Need to write this')
        code[row:] = docstring
    elif mode == 'insert':
        code.insert(row, docstring)
    else:
        options = ('replace', 'insert')
        raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
                         ''.format(mode=mode, options=options))

    return code
