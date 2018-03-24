#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..google import raises_block
from . import mixin


class Raises(mixin.SphinxBlockMixin, raises_block.Raises):
    pass
