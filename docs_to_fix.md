
#####
def get_required_tokens(self):
    '''list[str]: Get the tokens for this Context that must be filled.'''
    full_mapping_details = self.get_all_mapping_details()
    required_tokens = []

    for key, info in full_mapping_details.items():
        if info.get('required', True) and key not in required_tokens:
            required_tokens.append(key)

    return required_tokens


####

def foo():
    '''<os.join>: asdfasfd.'''
    return os.path.join('asdfd')

This is wrong.
1. It should be os.path.join
2. It should just be a string, not os.path.join!

####

    def visit_return(self, node):
        def is_yield_return(node):
            sibling = node.next_sibling()
            node_column_offset = node.col_offset

            while sibling is not None:
                is_in_same_statement = node_column_offset == sibling.col_offset
                if isinstance(sibling.value, astroid.Yield) and is_in_same_statement:
                    return True

                if not is_in_same_statement:
                    return False

                sibling = sibling.next_sibling()

            return False

        if is_yield_return(node):
            return

        function = node.scope()
        self.functions[function].setdefault('returns', [])
        self.functions[function]['returns'].append(node.value)



#### 
def split_into_parts(obj, split, as_type=tuple):
    
    obj = check.force_itertype(obj)
    obj = (part.strip() for obj_ in obj for part in obj_.split(split))
    return as_type(part for part in obj if part)


#### 
def split_hierarchy(obj, as_type=tuple):
    '''Split a hierarchy into pieces, using the "/" character.

    Args:
        obj (str or tuple[str]):
            The hierarchy to split.
        as_type (:obj:`callable`, optional):
            The iterable type to return the hierarchy.

    Returns:
        tuple[str]:
            The hierarchy, split into pieces.

    '''
    try:
        if obj[0] == HIERARCHY_SEP:
            items = itertools.chain(
                [HIERARCHY_SEP], split_into_parts(obj, split=HIERARCHY_SEP, as_type=list))
            return tuple(items)
    except IndexError:
        pass

    return split_into_parts(obj, split=HIERARCHY_SEP, as_type=as_type)


#### 


def import_object(name):
    '''Import a object of any kind, as long as it is on the PYTHONPATH.

    Args:
        name (str): An import name (Example: 'ways.api.Plugin')

    Raises:
        ImportError: If some object down the name chain was not importable or
                     if the entire name could not be found in the PYTHONPATH.

    Returns:
        The imported module, classobj, or callable function, or object.

    '''
    components = name.split('.')
    module = __import__(components[0])
    for comp in components[1:]:
        module = getattr(module, comp)
    return module


#### 
def decode(obj):
    '''dict[str]: Convert a URL-encoded string back into a dict.'''
    return conform_decode(six.moves.urllib.parse.parse_qs(obj))

def conform_decode(info):
    '''Make sure that 'create_using' returns a single string.'''
    return {key: value[0] if len(value) == 1 else value
            for key, value in six.iteritems(info)}


#### 


def encode(obj):
    '''Make the given descriptor information into a standard URL encoding.

    Args:
        obj (dict[str]): The Descriptor information to serialize.
        This is normally something like
        {'create_using': ways.api.FolderDescriptor}.

    Returns:
        str: The output encoding.

    '''
    # pylint: disable=redundant-keyword-arg
    return six.moves.urllib.parse.urlencode(obj, doseq=True)


#### 


    def get_child_tokens(self, token):
        '''Find the child tokens of a given token.

        Args:
            token (str): The name of the token to get child tokens for.

        Returns:
            list[str]: The child tokens for the given token. If the given token
                       is not a parent to any child tokens, return nothing.

        '''
        mapping_details = self.get_all_mapping_details()

        try:
            mapping = mapping_details[token].get('mapping', '')
        except KeyError:
            return []

        if mapping:
            return find_tokens(mapping)

        return []


#### Cross-attribute links
i.e. when you fill out the argument for "container", it will also fill out the
return-type with the same information (because we know that the two are LINKED)

def make_container_label(container, items_text):
    if items_text:
        return '{container}[{items_text}]'.format(
            container=container, items_text=items_text)

    return container


#### Recursive return-finding

def bar(thing=False):
	if thing:
		return ''
	return 8


def foo():
	'''bool or str: Info here.'''
	return bar()


The dream, baby!


#### Probably same as the one, above
def get_default_indent():
    return os.getenv('AUTO_DOCSTRING_INDENT', '    ')


#### This one, too

def drop_trailing_characters(text):
    # TODO : Allow ',' separated list
    characters = get_trailing_characters_to_drop()
    if text[len(characters):] == characters:
        return text[:len(characters)]
    return text


#### Logistical docstrings

def foo():
	for index in range(10):
		if index == 20:
			return index

This should be return index (int?) or NoneType - because there's a chance of
None


def foo():
	if thing:
		return 'asdf'
	elif other_thing:
		return True

should be return str or bool or NoneType


def foo():
	items = {
		'foo': False,
	}

	try:
		return items[name]	
	except KeyError:
		return []


should be bool or list, because those are the options
if `return []` is just `return`


def foo():
	items = {
		'foo': False,
	}

	try:
		return items[name]	
	except KeyError:
		pass

In this case, return is implied, because if we pass and there's nothing else,
then it would obviously return None


BUT

def foo():
	items = {
		'foo': False,
	}

	try:
		return items[name]	
	except KeyError:
		raise ValueError()

This is fine, because raise is another type of exit. And exiting in all cases
in the try/except is the same as if we returned. So it would not "also return
NoneType" implicitly ...!



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
	
We know the keys and most of the values. Both should work.

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

We know the keys / values of this dict, so we should know the output.

#### Some kind of attribute issue
def get_signals(widget, signal_type=QtCore.Signal, whitelist=None):
    signals = []
    for name in dir(widget):
        if whitelist is not None and name not in whitelist:
            continue

        attribute = getattr(widget, name)
        if isinstance(attribute, signal_type):
            signals.append(attribute)

    return signals
	

#### Nested call
    def get_current_shot_name(self):
        return self.shot_combo_b.lineEdit().text()


#### Nested call - Part Deux
    def get_current_shot_name(self):
		obj = self.shot_combo_b.lineEdit()
        return obj.text()


#### Bad characters
    def _validate_user_input(self, index, require_number=True):
        base_info = self.get_gui_info()

        shot_name = self.get_current_shot_name()

        try:
            shots_to_create = int(self.shot_number_widget.text())
        except ValueError:
            if require_number:
                raise ValueError('Shot must contain a number')
            else:
                shots_to_create = -1

        required_items = [
            (base_info['JOB'], 'job'),
            (base_info['SCENE'], 'scene'),
            (shot_name, 'shot name'),
            (shots_to_create, 'number of shots to make'),
        ]

        if str(index).lower() in ['all', 'everything']:
            index = len(required_items)

        missing_items_message = 'Item: "{item}" was missing. Could not create shots.'
        # TODO : Add some fancy stacktrace storing and a separate print to
        #        a terminal or logger, here
        missing_required_items = []
        for item, error_label in required_items[:index]:
            if not item:
                missing_required_items.append(missing_items_message.format(item=item))
                # TODO : add logging

        if missing_required_items:
            raise ValueError('\n'.join(missing_required_items))


#### Change `*args` to tuple[str] and `**kwargs` to dict[str]

    def format(self, *args, **kwargs):
        self._used_numbers = self._used_numbers.__class__()
        self._used_names = self._used_names.__class__()

        return super(NumberifyWordFormatter, self).format(*args, **kwargs)



#### Const.int(value=1) not supported. Add
    def _register_name_and_get_next_number(self, field_name='', stored_number=None):
        
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

#### Another
    @staticmethod
    def _tag(text):
        return text



#### This should know that it's always just a list
    @staticmethod
    def _get_all_args(node):
        try:
            decorators = node.decorators.get_children()
        except AttributeError:
            decorators = []

        children = list(node.args.get_children())

        drop_first_arg = isinstance(node.parent, astroid.ClassDef)

        if not drop_first_arg:
            return children

        for decorator in decorators:
            if decorator.name == 'staticmethod':
                return children

        return children[1:]

#### 
    @staticmethod
    def _include_message():
        try:
            return bool(int(os.getenv('AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE', '1')))
        except TypeError:
            return True

#### Maybe?


def get_ast_type(node):
    all_types = {
        astroid.BoolOp: bool,
    }

    try:
        return all_types[type(node)]
    except KeyError:
        raise NotImplementedError('Node: "{node}" is not supported yet.'.format(node=node))


#### More!


def add_docstring(code, row, style='', mode='replace'):
    '''Add an auto-generated docstring to the given `code`, at the given `row`.

    Args:
        code (str):
            The code to create a docstring for.
        row (int):
            The point in the code to create a docstring for.
        style (:obj:`str`, optional):
            The style to use to create the docstring. If no style is given,
            a default style is used from the `AUTO_DOCSTRING_STYLE`
            environment variable. If that variable isn't set,
            the code-style defaults to "google".
        mode (:obj:`str`, optional):
            "insert" - Adds the docstring above the given `row`.
            "replace" - Replaces the text at the given `row` with the docstring.

    Raises:
        ValueError: If the given `mode` was invalid.

    Returns:
        str: The auto-generated, UltiSnips docstring.

    '''
    code = list(code)
    docstring = create_docstring(code=code, row=row, style=style)

    if mode == 'replace':
        raise NotImplementedError('Need to write this')
        # code[row:] = docstring
    elif mode == 'insert':
        code.insert(row, docstring)
    else:
        options = ('replace', 'insert')
        raise ValueError('Mode: "{mode}" is unsupported. Options were, "{options}".'
                         ''.format(mode=mode, options=options))

    return code


#### attribute raise

class Foo(object):

	bar = 'ttt'


def foo():
	raise ValueError(Foo.bar)



#### method raise
todo : write example



#### Another situation

def thing(mode):
	'''

	Args:
		mode (str):
			'whatever': 
			'another': 
			'fff': 
			'ttt': 

	'''
	if mode == 'whatever':
		pass
	elif mode == 'another':
		pass
	elif thing and mode == 'fff':
		pass
	elif (not thing.endswith('aa') and bar) or mode == 'ttt':
		pass


#### This is saying return is NoneType, but it shold be wrapper. I think ...
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


#### Two things here

First off, WRAPPER_UPDATES and WRAPPER_ASSIGNMENTS should be tuple[str],
not tuple
Second, wrapper's return type should be <wrapper> not NoneType

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper



#### Got a NoneTypeError

This should be able to find the type from `_blocks`

    @classmethod
    def _get_block(cls, block):
        try:
            return cls._blocks[block]
        except KeyError:
            return

Also, make sure this works with a regular dict, too, not just a
classproperty

Also, this should pass safely, even if `_blocks` is an empty dict
