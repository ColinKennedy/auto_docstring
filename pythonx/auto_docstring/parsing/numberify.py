#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import re

# IMPORT LOCAL LIBRARIES
from . import ultisnips_build
from ..config import common
from ..core import check


class RecursiveNumberifyParser(ultisnips_build.RecursiveParser):

    _conversion_compiled = re.compile(r'(?P<number>\d*)(?P<text>.*)(?P<conversion>!\w)$')

    def __init__(self):
        super(RecursiveNumberifyParser, self).__init__()
        self._used_names = dict()
        self._used_numbers = set()

    @classmethod
    def _get_conversion_info(cls, text):
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

            try:
                is_convertible = self._is_list_convertible(items)
            except AttributeError:
                # If this happens, it's because items is a nested list
                # Since lists are recursively processed by _add_conversion, it's
                # OK to just set this value to False. Other recursion levels
                # will sort it out
                #
                is_convertible = False

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
