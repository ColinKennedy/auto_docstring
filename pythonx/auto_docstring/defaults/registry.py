#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import six


_KNOWN_TYPES = dict()


def get_default(obj, default=None):
    def return_obj(obj, *args, **kwargs):
        return obj

    try:
        value = _KNOWN_TYPES[obj]
    except KeyError:
        return default

    if isinstance(value, six.string_types):
        return functools.partial(return_obj, value)

    return value


def deregister_all():
    _KNOWN_TYPES.clear()


def register(obj, returns):
    _KNOWN_TYPES[obj] = returns
