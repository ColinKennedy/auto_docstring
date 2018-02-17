#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Create a docstring for a Python class, method, or function, automatically.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from .code_parser import (CollectorPython, ParserPython)
from .code_style import GoogleStylePython
from .docstring_builder import DocstringPython


BUILDERS = \
    {
        'python': DocstringPython,
    }
COLLECTORS = \
    {
        'python': CollectorPython
    }
PARSERS = \
    {
        'python': ParserPython,
    }
STYLES = \
    {
        'python':
            {
                'google': GoogleStylePython,
            }
    }


def get_code_block_from_lines(lines):
    '''Get all Python code blocks, leading up to the global namespace.

    Warning:
        The lines given to this function must not be formatted in any way
        (like with textwrap.dedent or lstrip()). It'll affect the way that
        this function executes.

    Args:
        lines (list[str]): The lines of code to check. If the lines never reach

    '''
    last_line = None
    for index, line in enumerate(lines):
        if not line.strip():
            last_line = index
        if last_line is not None and line.strip() != line:
            break

    try:
        return lines[:last_line]
    except KeyError:
        return lines


def get_builder(code, row, language, style):
    language = language.lower()
    style = style.lower()

    collector = COLLECTORS.get(language)
    if collector is None:
        raise ValueError(
            'Language: "{par}" does not have a valid collector. '
            'Options were, "{opt}".'.format(
                par=language, opt=sorted(COLLECTORS.keys())))
    parsed_code = collector.parse(code, row=row)

    parser = PARSERS.get(language)
    if parser is None:
        raise ValueError(
            'Language: "{par}" does not have a valid parser. '
            'Options were, "{opt}".'.format(
                par=language, opt=sorted(PARSERS.keys())))
    parsed_code = parser(parsed_code, row)

    style_object = STYLES.get(language, dict()).get(style)
    if style_object is None:
        raise ValueError('Style: "{sty}" was not valid. Options were, "{opt}".'
                         ''.format(sty=style, opt=sorted(STYLES.keys())))

    builder = BUILDERS.get(language)
    if builder is None:
        raise ValueError('Language: "{lang}" has no builder. Language options '
                         'were, "{opt}".'.format(lang=language,
                                                 opt=sorted(BUILDERS.keys())))
    return builder(parser=parsed_code, style=style_object)


def create_auto_docstring(code, row, language, style, blocks='*'):
    # '''Build a docstring, automatically, for some code.

    # Args:
    #     code (str): The code to create an automatic docstring of.
    #     row (int): The cursor's position, relative to the code.
    #     language (str): The language to assume that the code is.
    #                     This argument will be used to get a parser class
    #                     in order to parse the code.
    #     style (str): The style to draw the docstring in. Suggestion: 'google'.

    # Returns:
    #     str: The automatic docstring generated.

    # '''
    builder = get_builder(
        code=code, row=row, language=language, style=style)
    return builder.create_docstring(blocks)


def create_auto_docstring_block(code, row, language, style, block):
    builder = get_builder(
        code=code, row=row, language=language, style=style)
    return builder.create_docstring_block(block)
