TODO Make a table of contents for the docs
Make the first demo asciinema into a GIF

Welcome to vim-auto_docstring, and interactive Python-docstring auto-generator.

The tool supports sphinx-style docstrings as well as Google, numpy, and epydoc
styles.

To use the auto-generator, just place your cursor in the function that you want
to create documentation for and run the auto_docstring command.

[![demo](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd.png)](https://asciinema.org/a/AeIPtOBsBPuEHsPvUZqDQXwDd?autoplay=1&t=1)


# Installation

auto_docstring is an extension for UltiSnips, which is a Vim plugin that
generates text-snippets. Visit [the UltiSnips GitHub page](https://github.com/SirVer/ultisnips) for its latest installation requirements and instructions.

Once that is installed, install auto_docstring's dependencies, with [pip](https://pypi.python.org/pypi/pip).

```bash
$ pip install astroid
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


def get_auto_docstring_block(block):
    '''Generate a part of a docstring at the current row, in a Vim buffer.

    Args:
        block (str): The block to create. Example: 'Args'.

    '''
    (row, _) = vim.current.window.cursor
    docstring = class_read.create_auto_docstring_block(
        code='\n'.join(list(vim.current.buffer)), row=row,
        language='python', style='google', block=block)
    formatter = ultisnips_build.UltiSnipsTabstopFormatter()
    return formatter.format(docstring)

endglobal


post_jump "snip.expand_anon(get_auto_docstring())"
snippet ad "Create an automatic docstring, in Python"
endsnippet

```

And that's it, you should be able to get started immediately.
Of course, you can rename "snippet ad" to be whatever you'd like.


# Features

This tool is WIP but already has plenty of features

- Supports sphinx, numpy/scipy, Google, and epydoc docstring styles

TODO sphinx doesn't work. Why?

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


## Config Settings

### Behavior Config Settings

`AUTO_DOCSTRING_STYLE` Default: `google`

Options: ("google", "sphinx", "numpy", "epydoc")

The style to use to render the auto-generated docstring.
You can add your own styles and register them if you want (Seealso)
TODO make the feature to let people register their own styles ...
If you do make your own style, you can use it for this setting.

`AUTO_DOCSTRING_FOLLOW` Default: `1`

If '1', this will search through callable objects to get the actual type
If '0', it will just return the object/variable name, directly

`AUTO_DOCSTRING_AUTO_RAW_PREFIX` Default: `1`

Add 'r' to the docstring tag if the docstring contains '\'

`AUTO_DOCSTRING_BLOCK_ORDER` Default: `args,raises,returns,yields`

The comma-separated list to use to display docstring blocks.
You can specify block-order per-style, like this:

`google:args,raises,returns,yields:sphinx:args,returns,raises`

Or just define the list once and it will be applied for every style

`args,raises,returns,yields`

TODO Make a list of all the other allowed blocks for each style and also make
a function for that.


### Style Config Settings

`AUTO_DOCSTRING_DELIMITER` Default: `"""`

The text which is used to start and end the docstring


`AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE` Default: `1`

If '1' and a string could be found a raised exception then add that to the
auto-generated docstring.
If '0', do not include the message, even if there is one


`AUTO_DOCSTRING_REMOVE_TRAILING_CHARACTERS` Default: `.`

Character(s) to remove at the end of a raised exception's message. This
setting does nothing when `AUTO_DOCSTRING_INCLUDE_RAISE_MESSAGE` is set to '0'.


`AUTO_DOCSTING_TYPE_ORDER` Default: `ascending`

Options: ("ascending", "descending", "alphabetical")

If "ascending" then the returned types are listed by where they occur in the
source-file, sorted by line number. If "descending" then the sort is reversed.
If "alphabetical" then line number is ignored and it is sorted by-name.


### Syntax Config Settings

`AUTO_DOCSTRING_THIRD_PARY_PREFIX` Default: `<`

If a docstring is generated and the type of an object cannot be inferred,
this character will be placed at the beginning to tell the user "this is
undefined".


`AUTO_DOCSTRING_THIRD_PARY_SUFFIX` Default: `>`

If a docstring is generated and the type of an object cannot be inferred,
this character will be placed at the end to tell the user "this is
undefined".


`AUTO_DOCSTRING_CONTAINER_PREFIX` Default: `[`

The character or phrase that is used to

`AUTO_DOCSTRING_CONTAINER_SUFFIX`


`AUTO_DOCSTRING_OPTION_SEPARATOR` Default: `" or "`


`AUTO_DOCSTRING_DESCRIPTION_SEPARATOR` Default: `' '`

The text that gets placed between an argument + its type and the tabstop that
is used for its message.

AUTHOR-NOTE: Show what this looks like

