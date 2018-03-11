#### (I think this is a bug with) a variable + .format() in raises

    @classmethod
    def _build_plugins(cls, source, name, info, assignment):
        '''Create a Plugin or multiple Plugin objects.

        This method is meant to be used with get_plugins. It just exists
        to make it get_plugins more readable.

        Args:
            source (str):
                The location to a file on disk that defined plugin.
            name (str):
                The key that was used in the Plugin Sheet file where the plugin
                was defined.
            info (dict[str]):
                Any data about the plugin to include when the Plugin initializes.
                "uses" is retrieved to figure out if plugin is an absolute or
                relative plugin.
            assignment (str):
                The placement that this Plugin will go into.

        Returns:
            list[:class:`ways.api.DataPlugin`]:
                The generated plugins. It will make one Plugin object if
                info.get('uses', []) is empty. If "uses" is not empty, it will
                create one Plugin for each item in "uses".

        '''
        duplicate_uses_message = 'Plugin: "{plug}" has duplicate hierarchies ' \
                                 'in uses, "{uses}". Remove all duplicates.'

        plugins = []
        # There are two types of Context-Plugins, absolute and relative
        # If a plugin has 'uses' defined, that plugin is relative
        # because it needs another plugin/Context to function.
        #
        # We use all Context hierarchies defined in 'uses' to create
        # absolute plugins from each relative plugin
        #
        uses = info.get('uses', [])
        if uses:
            duplicates = _get_duplicates(uses)

            # TODO : "if duplicates:" stops bugs from happening
            #        if a user wrote a plugin that has duplicate items in
            #        'uses'. Ways likes to think that this is usually a
            #        copy/paste accident and is not intentional.
            #        and should never be intentional
            #
            #        Raising an error is really bad so we instead
            #        should just "continue" and log the failure so that
            #        a user can look it up, later
            #
            if duplicates:
                raise ValueError(duplicate_uses_message.format(
                    plug=name, uses=duplicates))

            for hierarchy in uses:
                if is_invalid_plugin(hierarchy, info):
                    continue

                context = sit.get_context(
                    hierarchy, assignment=assignment, force=True)
                info_ = cls._make_relative_context_absolute(info, parent=context)

                plugin = plug.DataPlugin(
                    name=name,
                    sources=(source, ),
                    info=dict_classes.ReadOnlyDict(info_),
                    assignment=assignment)
                plugins.append((plugin, assignment))
        else:
            plugin = plug.DataPlugin(
                name=name,
                sources=(source, ),
                info=dict_classes.ReadOnlyDict(info),
                assignment=assignment)
            plugins.append((plugin, assignment))

        return plugins


#### 1 - working with built-in methods of objects
    @classmethod
    def is_a_def_line(cls, allow_indent=True):
        '''Determine if the current line is a definition statement.

        TODO:
             This line is meant to just be temporary. Ideally, this should
             actually be replaced with regex.

        TODO:
            Put this function someplace else

        Args:
            allow_indent (bool): If False, only global functions will be True

        Returns:
            bool: Whether or not the line is a definition line

        '''
		line = 'some text'
        if not allow_indent:
            return False

        return line.strip().startswith(cls.def_startswith)
    # end is_a_def_line


#### Also check that "in" works correctly


#### ListComp
def _get_duplicates(obj):
    
    return [item for item, count in collections.Counter(obj).items() if count > 1]

AND other comps, like a set(generator) or dict(generator) etc etc


#### 2 - a list with a dict inside of it
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

#### 3 - an unknown return object-type

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


#### 4 - this should be parseable
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
