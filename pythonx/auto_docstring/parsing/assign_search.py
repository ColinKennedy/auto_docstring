#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A suite tools for finding assignments, in Python.

Sometimes, astroid has trouble inferring the types of Name variables and
it becomes necessary to "search" for these variables directly.

This module is made to assist this process.

'''

# IMPORT THIRD-PARTY LIBRARIES
import astroid


class AssignmentVisitor(object):

    '''A node visitor that captures `astroid.Assign` nodes.'''

    def __init__(self, *args, **kwargs):
        '''Create a blank list of assignments to store nodes into.'''
        super(AssignmentVisitor, self).__init__(*args, **kwargs)
        self.assignments = []

    def visit_assign(self, node):
        '''Store the given `astroid.Assign` node.'''
        self.assignments.append(node)

    def visit(self, node):
        '''Find all `astroid.Assign` nodes in the given `node`, recursively.'''
        for child in node.get_children():
            try:
                child.accept(self)
            except AttributeError:
                self.visit(child)


# TODO : This can probably be moved or replaced with visit.get_type
def get_ast_type(node):
    '''Convert the given statement `node` to a Python type.

    Raises:
        NotImplementedError: If the given `node`'s type is not found.

    Returns:
        The found type.

    '''
    all_types = {
        astroid.BoolOp: bool,
    }

    try:
        return all_types[type(node)]
    except KeyError:
        raise NotImplementedError('Node: "{node}" is not supported yet.'.format(node=node))


def get_assign_names(node):
    '''Find the name of every assigned variable, given some node.

    This function returns a list to account for Python's multi-assignment syntax
    example: a, b = True.

    Args:
        node (`astroid.Assign`): The object that contains assignments.

    Returns:
        list[str]: The names of every variable in the assignment.

    '''
    visitor = astroid.as_string.AsStringVisitor(indent='')
    return [n.accept(visitor) for n in node.targets]


def find_node_type(node, name):
    '''Try to find the node type of the given node, given some name.

    Basically, give this function a `astroid.FunctionDef` and the name of
    an assigned variable and it should give back that assigned variable's type.

    Args:
        node (`astroid.NodeNG`):
            The outer-scope (usually, a FunctionDef) to search within.
        name (str):
            The name of the variable to find an assignment of.

    Raises:
        RuntimeError: If `name` was not assigned within `node`.

    Returns:
        The found type.

    '''
    visitor = AssignmentVisitor()
    visitor.visit(node)

    matches = []
    for assign in visitor.assignments:
        if name in get_assign_names(assign):
            matches.append(assign)

    # We reverse the matches because the last assignment will always be the most
    # current assignment
    #
    for assign in reversed(matches):
        return get_ast_type(assign.value)

    raise RuntimeError('Node/Name: "{node}/{name}" was not found.'.format(
        node=node, name=name))
