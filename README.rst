Config info
- Remove "self._make_code" from unittests, since it's gross.
- rename the classes in common_block to be "Iterable" and "Container" since
  those terms describe those two much better

- support other documentation types (sphinx, numpy, scipy, epytext)
- allow the user to start docstrings on the next line + indentation, not the current line
 - this should work even in other documentation types

- Offer some kind of mechanism to allow default values to be displayed in the
  actual default parameter(s)

- Create a list of stdlib functions and objects to define the type of

Roadmap
 - cross-typing (between args and returns, for example)
 - Follow module function(s)
  - make sure that this works even with relative imports!
 - list/dict comprehensions
 - generators
 - logistical returns
 - attribute options




- ard - replaces the docstring in the function
- acd - only updates if args/raise statements are removed/added
  - otherwise, keeps the info of the docstring intact
- Make a function to create a specific docstring block type, instead of the
  entire docstring
  - make "acd"-esque variants for each, so that it can reuse parts of the block
- make sure these commands will work in VISUAL mode, too







## The new plan
Docstrings will be built in several phases
  1. parse with AST
  2. Get the types back
   - Be incredibly greedy about finding types. If need be, IMPORT and find the
	 types, that way. Get back classes and functions and objects, NOT strings
  3. Give the types to the block and let the block unpack and display them
  4. Build a Python format string from this information
  5. Build a UltiSnips string, from the Python format string


### Blocks ...
Define the classes you want and then "register" it to a particular style
Then define the "block-list" in an env var, to show the order of blocks to
display
 - If people don't provide their own block order, I'll just make some defaults


## New file structure
|- visit.py (1/2. contains the logic needed to find the types of things and get them)
|- collect.py (4)
|- converters
     |
	 +- ultisnips.py

|- blocks (3)
     |
     |
	 +---- google
	         |
			 + args.py
			 + returns.py
			 + yields.py
			 + raises.py
	 |
     +---- sphinx
	         |
			 + params.py
			 + rtype.py


- Gather as much as possible from the code
 - Returns
  - Get built-in, known types
  - If it's a called type, such as "asdfasdf".format() - If we know the method
	is a method of a built-in type, we should know what the method returns
  - A standard, importable object
   - a class
    - example:
	 from collections import OrderedDict
	 # ...
	 return OrderedDict()

	 The string should know that that's collections.OrderedDict!!!
   - a function (or other object)
    from itertools import islice
	islice([1,2,3,4,5], 3)

	should be itertools.islice
  - A third-party thing
   import some_module

   return some_module.THING

   # ...
   # in the docstring, it should continue to say "some_module.THING" unless the
   user has an env var set to "follow" the type. In which case, we find out
   what type some_module.THING is and use that, instead


## Immediate things to change

- There needs to be better config options. Being able to turn on / off type
  wrappers for things like :class`collections.OrderedDict` is vital.
- Tabstops should be consistent. I shouldn't skip a tabstop just because I knew
  exactly what type something was. It should still give me the option to visit
  that part of the string

In general, it just doesn't work on code as well as it needs to. The code is
not flexible. There was even a point where it errors because there was a "." in
the string that was being formatted. Disgraceful


## Config var notes
list[str]

list of str

AUTO_DOCSTRING_ITER_PREFIX
 - google default: '['
 - sphinx default: ' of '
AUTO_DOCSTRING_ITER_SUFFIX
 - google default: ']'
 - sphinx default: ''


AUTO_DOCSTING_TYPE_ORDER
 - default: "ascending"
 - other option: "alphabetical"
 - other option: "descending"
AUTO_DOCSTRING_STYLE = 'google'
AUTO_DOCSTRING_DELIMITER
 - default: '"""'
AUTO_DOCSTRING_THIRD_PARY_PREFIX = ''
 - could be '<'
AUTO_DOCSTRING_THIRD_PARY_SUFFIX = ''
 - could be '>'
AUTO_DOCSTRING_MAX_LINE_LENGTH = '79'
AUTO_DOCSTRING_BLOCK_ORDER = 'google:args,raises,returns,yields:'
 - if no type is given, just assume it's the current type, instead
AUTO_DOCSTRING_SIMPLIFY_RETURN_TYPES
 - default: '1'
AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE
 - default: '1'
AUTO_DOCSTRING_FOLLOW
 - default: "third-party,built-in"
AUTO_DOCSTRING_AUTO_RAW_PREFIX = '1'
AUTO_DOCSTRING_QUALIFIED_TYPES
 - default: "full"
 - options: "full", "simple"
AUTO_DOCSTRING_CLASS_TAG
 - default: ""
 - could be something like ":class:`{}`"
 - no {}? Then just append
AUTO_DOCSTRING_FUNCTION_TAG
 - default: ""
 - could be something like ":func:`{}`"
 - no {}? Then just append
AUTO_DOCSTRING_OBJECT_TAG
 - default: ""
 - could be something like ":obj:`{}`"
 - no {}? Then just append
AUTO_DOCSTRING_VARARG_PREFIX
 - default: `"*"`
AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS
 - default: '.'
AUTO_DOCSTRING_NESTED_TABSTOP_IN_ITERABLE
 - If 0, the effect is this: '{1:list[tuple[str]]!f}'
 - If 1, the effect is this: '{1:list[{2:tuple[str]!f}]!f}'
AUTO_DOCSTRING_NESTED_TABSTOP_IN_CONTAINER
 - If 0, the effect is this: '{1:list[tuple[str]]!f}'
 - If 1, the effect is this: '{1:list[{2:tuple[str]!f}]!f}'
AUTO_DOCSTRING_NESTED_TABSTOP_IN_RAISE
 - If 0, the effect is this: 'ValueError: {1:Thing "whatever"!f}'
 - If 1, the effect is this: 'ValueError: {1:Thing "{2:whatever!f}"!f}'
AUTO_DOCSTRING_EXPAND_CONTAINER_ITEMS
 - it will print out each key/value items that it knows about, if possible
AUTO_DOCSTRING_AUTO_ARG_DETAILS
 - default: 0
AUTO_DOCSTRING_TYPE_FOLLOW
 - default: 1
 - Lets you look up function docstrings, recursively, like for example if a
   function returns the result of another function
   If False, the original function name will just be returned

spacing = int(os.getenv('AUTO_DOCSTRING_BLOCK_SPACING', '1'))
return os.getenv('AUTO_DOCSTRING_INDENT', '    ')


-| Variable for customizing the []s outer part of docstring. You can replace
  them to be completely different, or include whitespace, or whatever
-| option to "follow" third-party libraries to get their actual types
-| choose your style with a single config variable
 -| Google-style
 -| sphinx
 -| doxygen
 -| NumPy
 -| SciPy

- The option to apply/restrict PEP257 rules
-| option for adding wrapper text to indicate third-party objects (like how we
  do <>s around stuff)
-| Max LL
- How to add "optional" info (?)
-| description tabstop location (below or in-line)
-| block-order
-| Need a config var for whether you want to simplify return types. For
   example, if you want to support list[tuple[str, int]]. Like that
-| raises - includes the origin message
- The format for how to write "default values" into docstrings, if at all
 - and what to do for explicit Python types, like True, False, None
-| use ''' or """
-| follow arg types that are variables, for example (like a global variable
  being used as a default)
   - make this separate from the other follow types
-| auto-check text (for example, if it contains \ anywhere, prefix delimiter
  with 'r')
-| do full, qualified types or types that are relative to the file

  example:
  ```
  from itertools import islice
  def foo():
       '''<itertools.islice>'''

  def foo():
       '''<islice>'''

  ```
