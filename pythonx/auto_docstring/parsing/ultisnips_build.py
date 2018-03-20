#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import pyparsing
import six

# IMPORT LOCAL LIBRARIES
from ..core import check
from ..config import common


class RecursiveParser(object):

    conversion_text = '!f'

    def __init__(self):
        super(RecursiveParser, self).__init__()

    @classmethod
    def _is_convertible(cls, item):
        return item.endswith(cls.conversion_text)

    @classmethod
    def _is_list_convertible(cls, items):
        try:
            return cls._is_convertible(items[-1])
        except IndexError:
            return False

    @classmethod
    def _convert(cls, text, force=False):
        ends_with_conversion = cls._is_convertible(text)
        if not force and not ends_with_conversion:
            return text

        if ends_with_conversion:
            text = text[:-2]  # Strip off the '!f'

        return text

    @staticmethod
    def _wrap(items):
        # This try/except is a very unique syntax to UltiSnips. Basically, if a
        # tabstop in UltiSnips contains text, it looks like this "${3:foo}" where
        # "foo" is default text. If the tabstop is just a number though, you can
        # write it as either "${3}" or just "$3". This try/except will check
        # if we actually need {}s. The prefix "$" will be added, later.
        #
        try:
            is_single_list = check.is_itertype(items) and len(items) == 1
            if is_single_list and items[0].isdigit():
                return items[0]
        except AttributeError:
            pass

        if isinstance(items, six.string_types) and items.isdigit():
            return items

        return '{{{}}}'.format(''.join(items))

    @staticmethod
    def _tag(text):
        return '$' + text

    def expand(self, items, force_convert=False):
        if not check.is_itertype(items):
            return items

        is_convertible = self._is_list_convertible(items)

        for index, item in enumerate(items):
            expanded_item = self.expand(item, force_convert=force_convert or is_convertible)
            items[index] = expanded_item

        # Re-add the "{}"s that pyparsing removed
        items = self._convert(''.join(items), force=force_convert)
        output = self._wrap(items)

        # Is this is going to be used as an UltiSnips snippet, add the $
        if is_convertible:
            output = self._tag(output)

        return output

    def _parse(self, text, function):
        # 1. We wrap the entire text in {}s, to make it a nested expression
        text = self._wrap(text)

        pyparsing.ParserElement.setDefaultWhitespaceChars('\n\t')
        _content = pyparsing.CharsNotIn(['{', '}'])
        _curlys = pyparsing.nestedExpr('{', '}', content=_content)

        # 2. Since we made the expression nested a little while ago, lets unpack it
        parsed_text = _curlys.parseString(text).asList()[0]
        result = function(parsed_text)

        # 3. The {}s that we added with `_wrap` need to be removed. So [1:-1] the result
        return result[1:-1]

    def parse(self, text, force_convert=False):
        function_to_run = functools.partial(self.expand, force_convert=force_convert)
        return self._parse(text, function_to_run)
