#!/usr/bin/env python
#


class NumpyMixin()
    @classmethod
    def _build_docstring_lines(cls, lines):
        output = []
        for arg, value in lines:
            output.extend(cls._make_lines(arg=arg, value=value))

        return output

    @classmethod
    def get_starting_lines(cls):
        header = cls.label
        return [header, '-' * len(header)]
