#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The module used to add default values for unparseable Python objects.'''

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import six


_KNOWN_TYPES = dict()


def get_default(obj, default=None):
    '''Get the default, callable function for the given `obj`.

    If this function returns the default value, try running
    :func:`auto_docstring.register` on `obj`, first.

    Args:
        obj: The pre-registered object to get the default value(s) of.
        default: The default value to return, if obj is not pre-registered.

    Returns:
        callable:

    '''
    def return_obj(obj, *args, **kwargs):
        '''Return the given object and ignore all other input.'''
        return obj

    try:
        value = _KNOWN_TYPES[obj]
    except KeyError:
        return default

    if isinstance(value, six.string_types):
        return functools.partial(return_obj, value)

    return value


def deregister_all():
    '''Forget all object default values.'''
    _KNOWN_TYPES.clear()


# TODO : Add to __init__.py
def register(obj, returns):
    '''Add a default value for the given `obj`.

    Args:
        obj:
            The key to store some default value. It's recommended to always
            pass a literal Python object, such as os.getenv, but if that is not
            possible, it is acceptable to use any key,
            like "os.getenv" (as a string).
        returns (callable[`astroid.Call` or `astroid.Name`] -> str or str):
            The default value that will be returned for this object.
            If a callable function is given then it must take a Call or Name
            object and parse it into a string.
            If the given object is a string, then it will just be returned.

    '''
    _KNOWN_TYPES[obj] = returns
