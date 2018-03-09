# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# '''Rebuild strings into UltSnips-compatible snippets.'''

# # IMPORT STANDARD LIBRARIES
# import string


# class UltiSnipsTabstopFormatter(string.Formatter):
#     def __init__(self):
#         super(UltiSnipsTabstopFormatter, self).__init__()
#         self._used_names = dict()
#         self._used_numbers = set()

#     def get_field(self, field_name, args, kwargs):
#         if '|' in field_name:
#             label = '${{{}}}'
#         else:
#             label = '${}'

#         label = label.format(field_name)
#         label = label.replace('|', ':')
#         return (label, field_name)

# IMPORT STANDARD LIBRARIES
import string

# IMPORT THIRD-PARTY LIBRARIES
from .core import check
import pyparsing


def _is_list_convertible(items):
    try:
        return items[-1].endswith('!f')
    except IndexError:
        return False


def _convert(text, force=False):
    ends_with_conversion = text.endswith('!f')
    if not force and not ends_with_conversion:
        return text

    if ends_with_conversion:
        text = text[:-2]  # Strip off the '!f'

    return text.replace('|', ':')


def _wrap(items):
    # This try/except is a very unique syntax to UltiSnips. Basically, if a
    # tabstop in UltiSnips contains text, it looks like this "${3:foo}" where
    # "foo" is default text. If the tabstop is just a number though, you can
    # write it as "${3}" or just "$3". This try/except will check if we actually
    # need {}s. The prefix "$" will be added, later.
    #
    try:
        if len(items) == 1 and items[0].isdigit():
            return items[0]
    except AttributeError:
        pass

    return '{{{}}}'.format(''.join(items))


def expand(items, force_convert=False):
    if not check.is_itertype(items):
        return _convert(items, force=force_convert)

    is_convertible = _is_list_convertible(items)

    for index, item in enumerate(items):
        items[index] = expand(item, force_convert=is_convertible)

    # Re-add the "{}"s that pyparsing removed
    output = _wrap(items)

    # Is this is going to be used as an UltiSnips snippet, add the $
    if is_convertible:
        output = '$' + output

    return output


def parse(text):
    # 1. We wrap the entire text in {}s, to make it a nested expression
    text = _wrap(text)

    pyparsing.ParserElement.setDefaultWhitespaceChars('\n\t')
    _content = pyparsing.CharsNotIn(['{', '}'])
    _curlys = pyparsing.nestedExpr('{', '}', content=_content)

    # 2. Since we made the expression nested a little while ago, lets unpack it
    parsed_text = _curlys.parseString(text).asList()[0]

    result = expand(parsed_text)

    # 3. The {}s that we added with `_wrap` need to be removed. So [1:-1] the result
    return result[1:-1]
