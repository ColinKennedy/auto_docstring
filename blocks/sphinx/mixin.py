#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SphinxBlockMixin(object):
    @classmethod
    def get_starting_lines(cls):
        return []

    @staticmethod
    def get_spacing():
        return 0
