#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import pyparsing
import six

# IMPORT LOCAL LIBRARIES
from . import common
from .core import check


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
        # write it as "${3}" or just "$3". This try/except will check if we actually
        # need {}s. The prefix "$" will be added, later.
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









# TODO : Split this into another file
# IMPORT STANDARD LIBRARIES
import re


class RecursiveNumberifyParser(RecursiveParser):

    _conversion_compiled = re.compile('(?P<number>\d*)(?P<text>.*)(?P<conversion>!\w)$')

    def __init__(self):
        super(RecursiveNumberifyParser, self).__init__()
        self._used_names = dict()
        self._used_numbers = set()

    @classmethod
    def _get_conversion_info(cls, text):
        output = dict()
        info = cls._conversion_compiled.match(text)
        try:
            return info.groupdict()
        except AttributeError:
            return dict()

    def _wrap(self, items):
        text = ''.join(items)
        return '{{{}}}'.format(text)

    def _convert(self, text, force=False):
        info = self._get_conversion_info(text)
        if not info:
            # If info is empty, we can safely return the original text
            return text

        conversion = info.get('conversion', '')

        latest_number = self._register_and_get_next_number(
            text=info.get('text', ''),
            stored_number=info.get('number', 0),
        )

        return '{latest_number}{text}{conversion}'.format(
            latest_number=latest_number,
            text=info.get('text', ''),
            conversion=conversion)

    @staticmethod
    def _tag(text):
        return text

    def _register_and_get_next_number(self, text='', stored_number=None):
        # '''Find the next number that this instance should use for formatting.

        # If `text` is not empty, check if the name was already used and,
        # if so, check what number was used and return it. If this is the first
        # time that `text` is used or `text` is empty, get
        # the next-available number.

        # Returns:
        #     int: The next number to use.

        # '''
        self._used_names.setdefault(text, dict())

        try:
            latest_number = max(self._used_numbers) + 1
        except ValueError:
            latest_number = 1

        if not text:
            self._used_names[text][stored_number] = latest_number
            self._used_numbers.add(latest_number)
            return latest_number

        try:
            return self._used_names[text][stored_number]
        except KeyError:
            self._used_names[text][stored_number] = latest_number
            self._used_numbers.add(latest_number)
            return latest_number

    def parse(self, text, force_convert=False):
        self.clear()
        return super(RecursiveNumberifyParser, self).parse(
            text=text,
            force_convert=force_convert)

    def add_conversion(self, text):
        # expected - text that doesn't already have !f on it
        def _add_conversion(items):
            if not check.is_itertype(items):
                return items

            is_convertible = self._is_list_convertible(items)

            for index, item in enumerate(items):
                items[index] = _add_conversion(item)

            if not is_convertible:
                items.insert(0, ':')
                items.insert(0, str(common.get_unique_number()))
                items.append(self.conversion_text)

            # Re-add the "{}"s that pyparsing removed
            output = self._wrap(items)
            return output

        output = self._parse(text, function=_add_conversion)
        # Remove the trailing !f that gets added
        output = output[:-2]
        return output

    def clear(self):
        self._used_names = self._used_names.__class__()
        self._used_numbers = self._used_numbers.__class__()
