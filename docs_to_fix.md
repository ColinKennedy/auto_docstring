

#### 1
    @classmethod
    def is_a_def_line(cls, line, allow_indent=True):
        '''Determine if the current line is a definition statement.

        TODO:
             This line is meant to just be temporary. Ideally, this should
             actually be replaced with regex.

        TODO:
            Put this function someplace else

        Args:
            line (str): The line to check if it's a definition line
            allow_indent (bool): If False, only global functions will be True

        Returns:
            bool: Whether or not the line is a definition line

        '''
        if not allow_indent and textmate.get_indent(line):
            return False

        return line.strip().startswith(cls.def_startswith)
    # end is_a_def_line


#### 2
    @classmethod
    def report(cls, filename):
        '''Return the given filename as data that Vim's quickfix window can use.

        Args:
            filename (str): The name of the file to report.

        Returns:
            list[dict[str]]: The information to add to Vim's quickfix window.

        '''
        return [
            {
                'filename': filename,
                'lnum': 1,
                'text': '{name} file: "{filename}"'.format(name=cls._key, filename=filename),
            },
        ]

#### 3

    @classmethod
    def process(cls, results):
        '''Select a part of the given results to write to disk and return.

        Args:
            results (dict[str]):
                The data to write to disk. Note: The given object must contain
                "cls._key" or this method will raise a KeyError.

        Returns:
            list[dict[str]]: The information to add to Vim's quickfix window.

        '''
        trace, exception = results.get(cls._key)

        if not trace or not exception:
            return dict()

        filename = write_data(trace, exception)
        return report_data(filename, trace, exception)


#### 4
    @staticmethod
    def make_quickfix_details(details):
        '''Change the given unpacked traceback data into a dict that Vim can use.

        Args:
            details (list[dict[str]]):
                'item' (str): The object / function / situation in the stack.
                'line' (int): The line number where the error occurred on.
                'source' (str): The location of where this error occurred.
                'text': The description of the line.

        Returns:
            list[dict[str]]:
                'text' (str): The description to use.
                'lnum' (int): The line, starting from the number 1.
                'filename' (str): The absolute or relative path to a file.

        '''
        output = []
        for item in details:
            text = item.get('text', '')
            output.append({
                'text': text.lstrip(),
                'lnum': item.get('line', 0),
                'filename': item.get('source', '')
            })

        return output
