#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module that contains classes and functions to convert Python strings.'''

# IMPORT STANDARD LIBRARIES
import re
import string


class NumberifyWordFormatter(string.Formatter):

    '''A string.Formatter object that converts {}s into numbers.

    Example:
        >>> formatter = NumberifyWordFormatter()
        >>> formatter.format("{} thing here {}")
        ... # Result: "{1} thing here {2}".

    Named fields will be given one, consistent number to share.

    Example:
        >>> formatter = NumberifyWordFormatter()
        >>> formatter.format("{name} {} here {name} {thing}")
        ... # Result: "{1|name} {2} here {1|name} {3|thing}")

    If named fields have unique numbers, then their numbers will not be shared.

    Example:
        >>> formatter = NumberifyWordFormatter()
        >>> formatter.format("{1|name} {} here {2|name} {thing}")
        ... # Result: "{1|name} {2} here {3|name} {4|thing}")

    Note:
        The use of "|" for named fields is custom to this class. Normal
        Python formatters won't know what to do with it so beware. You'll need
        to convert the "|" into something more useful, with another Formatter.
        See :mod:`auto_docstring.ultisnips_build` for an example.

    '''

    _field_name_compile = re.compile('(?:(?P<number>\d+)\|)?(?P<name>[^\|]+)?')

    def __init__(self):
        '''Create empty containers for used names and numbers.'''
        super(NumberifyWordFormatter, self).__init__()
        self._used_names = dict()
        self._used_numbers = set()

    def format(self, *args, **kwargs):
        '''Clear the last used-numbers and used-names and format the text.'''
        self._used_numbers = self._used_numbers.__class__()
        self._used_names = self._used_names.__class__()

        return super(NumberifyWordFormatter, self).format(*args, **kwargs)

    def format_field(self, obj, format_spec):
        return super(NumberifyWordFormatter, self).format_field(obj, format_spec)

    def get_field(self, field_name, args, kwargs):
        '''Create a numbered text from the given field.

        If `field_name` contains text, check if the name was already used and,
        if so, check what number was used and return it. If this is the first
        time that `field_name` is used or `field_name` is empty, get
        the next-available number.

        Note:
            If `field_name` is surrounded by "<>" characters then this method
            calls it "third-party". If a `field_name` is third-party, just pass
            its `replacement_text` along and don't do any further processing.
            Example: field_name: "<collections.OrderedDict>" would normally break
            a formatter but the added "<>"s allow it to process correctly.

        Args:
            field_name (str):
                The name of the field to replace. If the string was originally
                unnamed, like "{}", then `field_name` is "". If it is "{name}"
                then `field_name` is "name".
            args (tuple[str]): Unused in this method.
            kwargs (dict[str]): Unused in this method.

        Returns:
            tuple[str, str]:
                The text to replace `field_name` with and the `field_name`.

        '''
        match = self._field_name_compile.match(field_name)
        field_name = match.group('name') or ''
        number = self._register_name_and_get_next_number(field_name, match.group('number'))

        if field_name:
            replacement_text = '{' + str(number) + '|' + field_name + '}'
        else:
            replacement_text = '{{{number}}}'.format(number=number)

        kwargs = {field_name: replacement_text}

        if self._is_thirdparty_field(field_name):
            # If it's our special syntax, just pass the replacement text through
            output = (replacement_text, field_name)
        else:
            output = self._get_field(field_name, args, kwargs)

        return output

    @staticmethod
    def _is_thirdparty_field(name):
        '''bool: If the given name should not be processed by this instance.'''
        return name.startswith('<') and name.endswith('>')

    def _get_field(self, field_name, args, kwargs):
        '''Get the full, qualified field name from the given args.

        Args:
            field_name (str): The field to get the full object of.
            args (list[str]): The positional args.
            kwargs (dict[str]): The positional key/values for `field_name`.

        Returns:
            tuple[object, str]: The full, found object.

        '''
        first, rest = field_name._formatter_field_name_split()

        try:
            obj = self.get_value(first, args, kwargs)
        except KeyError:
            # If field_name is a nested string, like "list[str]", then just
            # pass it through without processing it
            #
            return (kwargs[field_name], first)

        return super(NumberifyWordFormatter, self).get_field(field_name, args, kwargs)

    def _register_name_and_get_next_number(self, field_name='', stored_number=None):
        '''Find the next number that this instance should use for formatting.

        If `text` is not empty, check if the name was already used and,
        if so, check what number was used and return it. If this is the first
        time that `text` is used or `text` is empty, get
        the next-available number.

        Returns:
            int: The next number to use.

        '''
        self._used_names.setdefault(field_name, dict())

        try:
            latest_number = max(self._used_numbers) + 1
        except ValueError:
            latest_number = 1

        if not field_name:
            self._used_names[field_name][stored_number] = latest_number
            self._used_numbers.add(latest_number)
            return latest_number

        try:
            return self._used_names[field_name][stored_number]
        except KeyError:
            self._used_names[field_name][stored_number] = latest_number
            self._used_numbers.add(latest_number)
            return latest_number
