#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import astroid


class AssignmentVisitor(object):
    def __init__(self, *args, **kwargs):
        super(AssignmentVisitor, self).__init__(*args, **kwargs)
        self.assignments = []

    def visit_assign(self, node):
        self.assignments.append(node)

    def visit(self, node):
        for child in node.get_children():
            try:
                child.accept(self)
            except AttributeError:
                self.visit(child)


# TODO : This can probably be moved
def get_ast_type(node):
    all_types = {
        astroid.BoolOp: bool,
    }

    try:
        return all_types[type(node)]
    except KeyError:
        raise NotImplementedError('Node: "{node}" is not supported yet.'.format(node=node))


def get_assign_names(node):
    visitor = astroid.as_string.AsStringVisitor(indent='')
    return [n.accept(visitor) for n in node.targets]


def find_node_type(node, name):
    visitor = AssignmentVisitor()
    visitor.visit(node)

    matches = []
    for assign in visitor.assignments:
        if name in get_assign_names(assign):
            matches.append(assign)

    # TODO : Pay attention to the docstring on this one. It's kind of special
    for assign in reversed(matches):
        return get_ast_type(assign.value)

    raise RuntimeError('Node/Name: "{node}/{name}" was not found.'.format(
        node=node, name=name))
