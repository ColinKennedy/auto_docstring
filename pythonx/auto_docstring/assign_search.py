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
    '''The main execution of the current script.'''
    visitor = AssignmentVisitor()
    visitor.visit(node)

    matches = []
    for assign in visitor.assignments:
        if name in get_assign_names(assign):
            matches.append(assign)

    for assign in reversed(matches):
        return get_ast_type(assign.value)


# def main():
#     '''The main execution of the current script.'''
# # IMPORT STANDARD LIBRARIES
# import textwrap
#     code = textwrap.dedent(
#         '''
#         def is_exe(fpath):

#             exe = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
#             # search for executable under windows
#             if not exe:
#                 if extList:
#                     for ext in extList:
#                         exePath = '%s%s' % (fpath, ext)
#                         if os.path.isfile(exePath) and os.access(exePath, os.X_OK):
#                             pathExt[0] = ext
#                             return True
#                     return False
#             return exe
#         ''')

#     node = astroid.parse(code)
#     visitor = AssignmentVisitor()
#     visitor.visit(node)
#     name = 'exe'

#     matches = []
#     for assign in visitor.assignments:
#         if name in get_assign_names(assign):
#             matches.append(assign)

#     for assign in reversed(matches):
#         return get_ast_type(assign.value)


# if __name__ == '__main__':
#     main()
