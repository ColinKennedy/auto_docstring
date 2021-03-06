#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The module that's responsible for add docstrings to source-code.'''

# IMPORT THIRD-PARTY LIBRARIES
import astroid

# IMPORT LOCAL LIBRARIES
from .config import common
from .parsing import visit
from .parsing import numberify
from .config import environment
from .parsing import ultisnips_build


def _needs_prefix(text):
    options = ('\r', '\t', '\n', '\b')
    for option in options:
        if option in text:
            return True

    return False


def create_docstring(code, row, style='', wrap=False):
    '''Create a docstring for the given `code`, at the specified `row`.

    Args:
        code (str): The code to create a docstring for.
        row (int): The point in the code to create a docstring for.
        style (:obj:`str`, optional):
            The style to use to create the docstring. If no style is given,
            a default style is used from the `AUTO_DOCSTRING_STYLE`
            environment variable. If that variable isn't set,
            the code-style defaults to "google".
        wrap (:obj:`bool`, optional):
            If True, add `"""` around the generated docstring.
            If False, do not add any delimiter around the generated docstring.
            Default is False.

    Returns:
        str: The auto-generated docstring.

    '''
    if not style:
        style = environment.get_current_style()

    # Parse the code
    node = astroid.parse(code)
    full_info = visit.get_info(node)
    node_that_needs_a_docstring = visit.get_closest_docstring_node(row, full_info)

    # Find the node's group and then get its info
    group = full_info['nodes'][node_that_needs_a_docstring]
    docstring_info = full_info[group][node_that_needs_a_docstring]

    # draw the docstring!
    style_object = common.create_code_style(style)
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
    #     '''{1!f}.
    #
    #     {2:name!f}
    #
    #     Args:
    #         foo ({3!f}): {2:name!f}.
    #
    #     '''
    #
    parser = numberify.RecursiveNumberifyParser()
    generated_docstring = parser.parse(initial_docstring)

    if wrap:
        delimiter = environment.get_docstring_delimiter()
        return delimiter + generated_docstring + delimiter

    return generated_docstring


def create_ultisnips_docstring(code, row, style='', wrap=False):
    '''Create an UltiSnips-style docstring for the given `code`.

    Args:
        code (str):
            The code to create a docstring for.
        row (int):
            The point in the code to create a docstring for.
        style (:obj:`str`, optional):
            The style to use to create the docstring. If no style is given,
            a default style is used from the `AUTO_DOCSTRING_STYLE`
            environment variable. If that variable isn't set,
            the code-style defaults to "google".
        wrap (:obj:`bool`, optional):
            If True, add `"""` around the generated docstring.
            If False, do not add any delimiter around the generated docstring.
            Default is False.

    Returns:
        str: The auto-generated, UltiSnips docstring.

    '''
    docstring = create_docstring(code, row, style=style)
    docstring = convert_to_ultisnips(docstring)

    # TODO : Once parsing has been fixed, remove this "if wrap:" condition
    # and get create_docstring do it, instead.
    #
    if wrap:
        delimiter = environment.get_docstring_delimiter()
        return delimiter + docstring + delimiter
    return docstring


def convert_to_ultisnips(code):
    '''Convert an auto-generated docstring to a UltiSnips-style docstring.'''
    return ultisnips_build.RecursiveParser().parse(code)


def add_docstring(code, row, style='', mode='replace'):
    '''Add an auto-generated docstring to the given `code`, at the given `row`.

    Args:
        code (str):
            The code to create a docstring for.
        row (int):
            The point in the code to create a docstring for.
        style (:obj:`str`, optional):
            The style to use to create the docstring. If no style is given,
            a default style is used from the `AUTO_DOCSTRING_STYLE`
            environment variable. If that variable isn't set,
            the code-style defaults to "google".
        mode (:obj:`str`, optional):
            "insert" - Adds the docstring above the given `row`.
            "replace" - Replaces the text at the given `row` with the docstring.

    Raises:
        ValueError: If the given `mode` was invalid.

    Returns:
        str: The auto-generated, UltiSnips docstring.

    '''
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
