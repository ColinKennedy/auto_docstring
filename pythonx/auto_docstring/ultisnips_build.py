# IMPORT THIRD-PARTY LIBRARIES
from .core import check
import pyparsing


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
            if len(items) == 1 and items[0].isdigit():
                return items[0]
        except AttributeError:
            pass

        return '{{{}}}'.format(''.join(items))

    @staticmethod
    def _tag(text):
        return '$' + text

    def expand(self, items, force_convert=False):
        if not check.is_itertype(items):
            return self._convert(items, force=force_convert)

        is_convertible = self._is_list_convertible(items)

        for index, item in enumerate(items):
            items[index] = self.expand(item, force_convert=force_convert or is_convertible)

        # Re-add the "{}"s that pyparsing removed
        output = self._wrap(items)

        # Is this is going to be used as an UltiSnips snippet, add the $
        if is_convertible:
            output = self._tag(output)

        return output

    def parse(self, text, force_convert=False):
        # 1. We wrap the entire text in {}s, to make it a nested expression
        text = self._wrap(text)

        pyparsing.ParserElement.setDefaultWhitespaceChars('\n\t')
        _content = pyparsing.CharsNotIn(['{', '}'])
        _curlys = pyparsing.nestedExpr('{', '}', content=_content)

        # 2. Since we made the expression nested a little while ago, lets unpack it
        parsed_text = _curlys.parseString(text).asList()[0]

        result = self.expand(parsed_text, force_convert=force_convert)

        # 3. The {}s that we added with `_wrap` need to be removed. So [1:-1] the result
        return result[1:-1]


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

    @staticmethod
    def _wrap(items):
        return '{{{}}}'.format(''.join(items))

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

    def clear(self):
        self._used_names = self._used_names.__class__()
        self._used_numbers = self._used_numbers.__class__()
