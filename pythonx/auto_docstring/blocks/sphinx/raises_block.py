#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT LOCAL LIBRARIES
from ..google import raises_block
from . import mixin


class Raises(raises_block.Raises, mixin.SphinxBlockMixin):
    pass
