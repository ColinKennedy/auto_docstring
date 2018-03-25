TODO Make a table of contents for the docs
Make the first demo asciinema into a GIF

Welcome to vim-auto_docstring, and interactive Python-docstring auto-generator.

The tool supports sphinx-style docstrings as well as Google, numpy, and epydoc
styles.

[![demo](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd.png)](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd?autoplay=1&t=1)


# How To Use
To use the auto-generator, just place your cursor wherever you want to create
the docstring and run the auto_docstring command.


# Installation

auto_docstring is an extension for UltiSnips, which is a Vim plugin that
generates text-snippets. Visit [the UltiSnips GitHub page](https://github.com/SirVer/ultisnips) for its latest installation requirements and instructions.

Once that is installed, install auto_docstring's dependencies, with [pip](https://pypi.python.org/pypi/pip).

```bash
$ pip install astroid
$ pip install pyparsing
```

Now add auto_docstring to your Vim configuration using a package manager.

## Vim-Plug

```vim
Plug 'ColinKennedy/vim-auto_docstring'
```

## Vundle

```vim
Plugin 'ColinKennedy/vim-auto_docstring'
```


Finally, because auto_docstring is a regular UltiSnips snippet, we need to add
the snippet to UltiSnips's list of Python snippets.

Open a Python file, any is fine, and then run `:UltiSnipsEdit` to open your
python.snippets file. Add this snippet defintion into it

TODO Make sure these snippets work + installation instructions

```vim
global !p
from auto_docstring import docstring_builder


def get_auto_docstring():
    '''Generate a docstring at the current row, in a Vim buffer.'''
    # return ''
    (row, _) = vim.current.window.cursor
    row -= 1
    code = '\n'.join(list(vim.current.buffer))
    docstring = docstring_builder.create_ultisnips_docstring(
        code, row=row, style='')
    return "'''" + docstring + "'''"
endglobal


post_jump "snip.expand_anon(get_auto_docstring())"
snippet ad "Create an automatic docstring, in Python"
endsnippet

```

And that's it, you should be able to get started immediately.
Of course, you can rename "snippet ad" to be whatever you'd like.


# Features

- Supports sphinx, numpy/scipy, Google, and epydoc (doxygen) docstring styles

TODO sphinx asciinema player isn't displaying... Why?

Sphinx
[![sphinx](https://asciinema.org/a/40b8QaBG949TFhIBxWk91Ub5p.kng)](https://asciinema.org/a/40b8QaBG949TFhIBxWk91Ub5p)

Numpy
[![numpy/scipy](https://asciinema.org/a/aOYKWOiD92Bz9XkixmhUOerd6.png)](https://asciinema.org/a/aOYKWOiD92Bz9XkixmhUOerd6)

Google
[![Google](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd.png)](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd)

Epydoc
[![epydoc](https://asciinema.org/a/Jpebcqy20XDTRf6pZlFmkLrzu.png)](https://asciinema.org/a/Jpebcqy20XDTRf6pZlFmkLrzu)

- classmethod/staticmethod recognition
- optional-arg parsing
- return-type grouping
- nested-function support
- follows local functions and objects to get its types

- most features are overridable or highly-configurable


## Config Settings

This repository is configurable using either environment variables or as
Vim variables. By default, Vim variables are preferred over any environment
variables. The environment variable option is a fallback, in case no vim
variables exist.

### Behavior Config Settings

env var: `AUTO_DOCSTRING_STYLE`
vim var: `g:auto_docstring_style`
Default: `google`

Options: ("google", "sphinx", "numpy", "epydoc")

The style to use to render the auto-generated docstring.
You can add your own styles and register them if you want (Seealso)
TODO make the feature to let people register their own styles ...
If you do make your own style, you can use it for this setting.

env var: `AUTO_DOCSTRING_TYPE_FOLLOW`
vim var: `g:auto_docstring_type_follow`
Default: `1`

If '1', this will search through callable objects to get the actual type
If '0', it will just return the object/variable name, directly

env var: `AUTO_DOCSTRING_AUTO_RAW_PREFIX`
vim var: `g:auto_docstring_raw_prefix`
Default: `1`

Add 'r' to the docstring tag if the docstring contains '\'

env var: `AUTO_DOCSTRING_BLOCK_ORDER`
vim var: `g:auto_docstring_block_order`
Default: `args,raises,returns,yields`

The comma-separated list to use to display docstring blocks.
You can specify block-order per-style, like this:

`google:args,raises,returns,yields:sphinx:args,returns,raises`

Or just define the list once and it will be applied for every style

`args,raises,returns,yields`

TODO Make a list of all the other allowed blocks for each style and also make
a function for that.


### Style Config Settings

env var: `AUTO_DOCSTRING_DELIMITER`
vim var: `g:auto_docstring_delimiter`
Default: `"""`

The text which is used to start and end the docstring


env var: `AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE`
vim var: `g:auto_docstring_`
Default: `1`

If '1' and a string could be found a raised exception then add that to the
auto-generated docstring.
If '0', do not include the message, even if there is one


env var: `AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS`
vim var: `g:auto_docstring_remove_trailing_characters`
Default: `.`

Character(s) to remove at the end of a raised exception's message. This
setting does nothing when `AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE` is set to '0'.


env var: `AUTO_DOCSTING_TYPE_ORDER`
vim var: `g:auto_docsting_type_order`
Default: `descending`

Options: ("ascending", "descending", "alphabetical")

If "ascending" then the returned types are listed by where they occur in the
source-file, sorted by line number. If "descending" then the sort is reversed.
If "alphabetical" then line number is ignored and it is sorted by-name.


### Syntax Config Settings

env var: `AUTO_DOCSTRING_THIRD_PARY_PREFIX`
vim var: `g:auto_docstring_third_pary_prefix`
Default: `<`

If a docstring is generated and the type of an object cannot be inferred,
this character will be placed at the beginning to tell the user "this is
undefined".


env var: `AUTO_DOCSTRING_THIRD_PARY_SUFFIX`
vim var: `g:auto_docstring_third_pary_suffix`
Default: `>`

If a docstring is generated and the type of an object cannot be inferred,
this character will be placed at the end to tell the user "this is
undefined".


env var: `AUTO_DOCSTRING_CONTAINER_PREFIX`
vim var: `g:auto_docstring_container_prefix`
Default: `[`

TODO finish description
The character or phrase that is used to

env var: `AUTO_DOCSTRING_CONTAINER_SUFFIX`
vim var: `g:auto_docstring_container_suffix`
Default: `]`

env var: `AUTO_DOCSTRING_OPTION_SEPARATOR`
vim var: `g:auto_docstring_option_separator`
Default: `" or "`


env var: `AUTO_DOCSTRING_DESCRIPTION_SEPARATOR`
vim var: `g:auto_docstring_description_separator`
Default: `' '`

The text that gets placed between an argument + its type and the tabstop that
is used for its message.

AUTHOR-NOTE: Show what this looks like


## Roadmap

The below list is the current set of planned features for auto_docstring.
Each version has a set number of features to implement.

To see the most recently implemented features, see the CHANGELOG


### 0.1

- Add dict-comprehension syntax support
- Allow docstrings with default args to include its default-arg as part of
  the docstring
- Let the user customize how / where that default arg information is
  displayed
- Allow the user to start docstrings on the next line + indentation, not the current line


### 0.2

```python
def foo():
	return 8
set((foo() for _ in range(10)))
```
should return a type of "set[int]"

- Follow modules recursively to get the types of objects
- Add support for local Python imports
- Allow class docstrings (like an attributes block / args block)
- Add type-inference for classmethods and instancemethods


### 1.0
- Add better support for standard library functions, classes, and objects
- Find a way to display individal docstring blocks, rather than generating
  an entire docstring all at once
- Support later versions of Python (3.X)
- R&D Type-hinting, for Python 3 (possibly add it as a goal for 0.4)
- Support generator syntax with cast types. For example


### 1.1
- Add convenience snippets such as ...
	- "ard" - Which replaces the docstring in the function
	- "acd" - Which will re-use an exising docstring and only add/remove members
	- These commands would work in VISUAL mode, too


### 1.2

- unclosed return detection
i.e.

```python
def foo():
	for item in range(bar):
		if item:
			return 'fizz'
```

Should be a return type of "str or NoneType" because there is a chance that the
if condition will not be True.
Whereas



```python
def foo():
	for item in range(bar):
		if item:
			return 'fizz'
	else:
		return False
```

Should be a returned for "str or bool" because the for-loop is closed

- Create a way to customize how ", optional):" tags are displayed
- Implement shared cross-typing across blocks

Example:
```python
def foo(item):
	return item
```

Should allow the user to replace "item" and have it update in both the "Args"
and "Returns" block at the same time, so they can save time writing variable types
