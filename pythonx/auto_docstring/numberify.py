#!/usr/bin/env python
#

# IMPORT STANDARD LIBRARIES
import string


class NumberifyWordFormatter(string.Formatter):
    def __init__(self):
        super(NumberifyWordFormatter, self).__init__()
        self._used_names = dict()
        self._used_numbers = set()

    def format(self, *args, **kwargs):
        self._used_numbers = self._used_numbers.__class__()
        self._used_names = self._used_names.__class__()

        return super(NumberifyWordFormatter, self).format(*args, **kwargs)

    def get_field(self, field_name, args, kwargs):
        number = self._get_next_number(field_name)
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

        self._used_names[field_name] = number
        self._used_numbers.add(number)

        return output

    @staticmethod
    def _is_thirdparty_field(name):
        return name.startswith('<') and name.endswith('>')

    def _get_field(self, field_name, args, kwargs):
        first, rest = field_name._formatter_field_name_split()

        try:
            obj = self.get_value(first, args, kwargs)
        except KeyError:
            return (kwargs[field_name], first)

        # loop through the rest of the field_name, doing
        #  getattr or getitem as needed
        for is_attr, i in rest:
            if is_attr:
                obj = getattr(obj, i)
            else:
                obj = obj[i]

        return obj, first

    def _get_next_number(self, text=''):
        try:
            latest_number = max(self._used_numbers) + 1
        except ValueError:
            latest_number = 1

        if not text:
            return latest_number

        try:
            return self._used_names[text]
        except KeyError:
            return latest_number
