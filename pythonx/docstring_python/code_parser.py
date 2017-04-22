#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module of parsers for coding languages. Currently only supports Python.'''

# IMPORT STANDARD LIBRARIES
import ast

NODE_TYPES = \
    {
        ast.Str: 'str',
        ast.List: 'list',
    }


class CollectorPython(object):

    '''Responsible for creating rich data from Python code text.'''

    def __init__(self):
        '''Initialize and do not create instance attributes.'''
        super(CollectorPython, self).__init__()

    @staticmethod
    def parse(code, row):
        '''Get the closest node in the code's Abstract Syntax Tree (ast).

        Args:
            code (str): The Python code to parse.
            row (int): The cursor's position, relative to the given code.

        Returns:
            <ast.Node> or NoneType: The node closest to the given row.

        '''
        tree = ast.parse(code)
        previous_node = None
        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                continue

            try:
                line_number = node.lineno
            except AttributeError:
                pass
            else:
                if line_number > row:
                    if previous_node is None:
                        return node
                    return previous_node
            previous_node = node
        return previous_node


class ParserPython(object):

    '''Take an ast collector and create an interface for grabbing its contents.

    In particular, all of the methods in this class will be used to

    '''

    def __init__(self, collector, row):
        '''Initialize the object with a collector, to query data from.

        Args:
            collector (CollectorPython):
                The collector to get parsed Python data from.

        '''
        super(ParserPython, self).__init__()
        self.collector = collector
        self.row = row

    def get_context(self, row=None):
        '''Create a description of where row is, in Python code.

        For example, if the row is located in a method of some class that is
        actually a classmethod, this function will return 'classmethod'.

        Args:
            row (:obj:`int`, optional): The row number to check the context of.
                                        If no row is given, it will default to
                                        the row stored within the parser.

        Returns:
            str: The closest description for the current row.

        '''
        if row is None:
            row = self.row

        row_type = self.get_row_type(row=row, recursive=True)
        context_types = \
            {
                ast.FunctionDef: 'function',
                ast.Module: 'module',
            }

        if isinstance(self.collector, ast.ClassDef):
            if isinstance(row_type, ast.FunctionDef):
                decorator_names = [dec.id for dec in row_type.decorator_list]
                if 'classmethod' in decorator_names:
                    return 'classmethod'
                elif 'staticmethod' in decorator_names:
                    return 'staticmethod'
                return 'method'
            elif isinstance(row_type, ast.Expr):
                return 'class_properties'
        return context_types.get(type(row_type), '')

    def get_info(self, node, node_type=''):
        class ExitVisitor(ast.NodeVisitor):

            types = NODE_TYPES

            def __init__(self, *args, **kwargs):
                super(ExitVisitor, self).__init__(*args, **kwargs)
                self.raises = []
                self.returns = []
                self.yields = []

            def visit_Raise(self, node):
                message = ''
                for arg in node.type.args:
                    message = arg.s
                    break
                self.raises.append(
                    {
                        'name': node.type.func.id,
                        'message': message,
                        'type': '',
                    })

            def visit_Return(self, node):
                self.returns.append(
                    {
                        'name': '',
                        'message': '',
                        'type': get_ast_type(node.value),
                    })

            def visit_Yield(self, node):
                self.yields.append(
                    {
                        'name': '',
                        'message': '',
                        'type': get_ast_type(node.value)
                    })

        args = []

        args_len = len(node.args.args)
        for index, arg in enumerate(node.args.args):
            try:
                type_ = node.args.defaults[-1 * index]
                if isinstance(type_, ast.Call):
                    type_ = '<{module}.{attr}>'.format(
                        module=type_.func.value.id, attr=type_.func.attr)
                else:
                    type_ = get_type_as_str(type(getattr(type_, type_._fields[0])))
            except IndexError:
                type_ = ''

            args.append(
                {
                    'name': arg.id,
                    'type': type_,
                    'message': ''
                })

        if node_type in ['method', 'classmethod']:
            try:
                args = args[1:]
            except IndexError:
                pass

        visitor = ExitVisitor()
        visitor.visit(node)
        raises = visitor.raises
        returns = visitor.returns
        yields = visitor.yields

        return \
            {
                'blocks':
                {
                    'Args': args,
                    'Raises': raises,
                    'Returns': returns,
                    'Yields': yields,
                }
            }

    def get_row_type(self, row=None, recursive=True):
        '''Get the most accurate, fine grain parse type for our code.

        For example, self.collector may be a Module or a ClassDef but the row
        may actually be a FunctionDef within the ClassDef. This method is meant
        to figure that out.

        Args:
            row (:obj:`int`, optional): The row to check. If no row is given,
                                        the current object's row is used.
            recursive (:obj:`bool`, optional):
                    If True, this method will continue calling itself until
                    the lowest level ast.Node is found. Default is True.

        Returns:
            <ast.Node>: The lowest-level node for this object/row.

        '''
        if row is None:
            row = self.row

        previous_node = None

        if isinstance(self.collector, ast.FunctionDef):
            return self.collector

        body = self.collector.body
        for node in body:
            if node.lineno > row:
                if previous_node is None:
                    return node
                return previous_node
            previous_node = node

        # If we made it this far, assume that the row is within the last
        # element of this parse node
        #
        return body[-1]


def get_ast_type(node):
    if isinstance(node, ast.Name):
        return get_type_as_str(type(eval(node.id)))

    return NODE_TYPES[node.__class__]


def get_type_as_str(object_type):
    return str(object_type)[7:-2]


if __name__ == '__main__':
    print(__doc__)

