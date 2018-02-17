#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module of parsers for coding languages. Currently only supports Python.'''

# IMPORT STANDARD LIBRARIES
import __builtin__
import pydoc
import ast
import re

# IMPORT THIRD-PARTY LIBRARIES
# TODO : Make a relative import
from core import grouping
from core import check
import six


class ExitVisitor(ast.NodeVisitor):

    types = \
        {
            ast.BoolOp: 'bool',
            ast.comprehension: 'list',
            list: 'list',
            ast.List: 'list',
            ast.Num: 'float',
            ast.Str: 'str',
            ast.Tuple: 'tuple',

            # built-in functions that will typically return an expected value
            'join': 'str',
            'rstrip': 'str',
        }

    def __init__(self, *args, **kwargs):
        super(ExitVisitor, self).__init__(*args, **kwargs)
        self.raises = []
        self.returns = []
        self.warnings = []
        self.yields = []

        self.visiting_node = None

    def visit(self, node, store=False):
        if store:
            self.visiting_node = node
        super(ExitVisitor, self).visit(node=node)

    def visit_Assign(self, node):
        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue

            if isinstance(target.value, ast.Attribute):
                # Example: self.something
                name = target.value.value.id + '.' + target.value.attr
                type_ = 'scoped'

            elif isinstance(target.value, ast.Name):
                name = target.value.id
                type_ = 'local'
            else:
                raise NotImplementedError(
                    'Target: "{target}" is not supported by assign.'
                    ''.format(target=target))

            self.warnings.append(
                {
                    'name': name,
                    'message': '',
                    'type': type_,
                })

    def visit_FunctionDef(self, node):
        for child_node in (node_ for node_ in ast.iter_child_nodes(node)
                           if not isinstance(node_, ast.FunctionDef)):
            self.visit(child_node)

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
        return_type = get_type_from_ast(node.value,
                                        parent=self.visiting_node)
        if not isinstance(return_type, six.string_types):
            # Note: We remove duplicates, here
            try:
                return_type = grouping.uniquify_list(return_type)
            except TypeError:
                pass
            return_type = get_type_as_str(return_type)
        else:
            return_type = '{' + return_type + '}'

        self.returns.append(
            {
                'name': '',
                'message': '',
                'type': return_type,
            })

    def visit_Yield(self, node):
        yield_type = get_type_from_ast(node.value,
                                       parent=self.visiting_node)
        if not isinstance(yield_type, six.string_types):
            yield_type = get_type_as_str(yield_type)
        else:
            yield_type = '{' + yield_type + '}'

        self.yields.append(
            {
                'name': '',
                'message': '',
                'type': yield_type,
            })


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
        walked_nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                continue

            if isinstance(node, ast.FunctionDef):
                for walk_node in walked_nodes:
                    for node_ in ast.walk(walk_node):
                        if isinstance(node_, ast.FunctionDef) and node == node_:
                            node.parent = walk_node
                            break

            try:
                # row is base 0 but line number is base 1 so offset by 1
                line_number = node.lineno - 1
            except AttributeError:
                pass
            else:
                if line_number > row:
                    break
            walked_nodes.append(node)

        return walked_nodes[-1]


class ParserPython(object):

    '''Take an ast collector and create an interface for grabbing its contents.

    In particular, all of the methods in this class will be used to

    '''

    def __init__(self, collector, row):
        '''Initialize the object with a collector, to query data from.'''
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
        try:
            parent = self.collector.parent
            has_parent = True
        except AttributeError:
            has_parent = False

        parent = None
        try:
            parent = self.collector.parent
        except AttributeError:
            pass

        if isinstance(self.collector, ast.ClassDef) or \
                (parent and isinstance(parent, ast.ClassDef)):
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
        visitor = ExitVisitor()
        visitor.visit(node, store=True)
        raises = visitor.raises
        returns = visitor.returns
        yields = visitor.yields
        warnings = visitor.warnings

        args = []
        args_len = len(node.args.args)
        defaults_len = len(node.args.defaults)
        offset_len = args_len - defaults_len

        for index, arg in enumerate(node.args.args):
            # Get the default argument (if any) for this arg
            defaults_index = index - offset_len
            type_ = ''
            if defaults_index >= 0:
                type_ = node.args.defaults[defaults_index]
                if isinstance(type_, ast.Call):
                    type_ = '<{module}.{attr}>'.format(
                        module=type_.func.value.id, attr=type_.func.attr)
                else:
                    arg_type = get_type_from_ast(type_, parent=visitor.visiting_node)
                    # Note: We are removing duplicate arg types, here
                    try:
                        arg_type = grouping.uniquify_list(arg_type)
                    except TypeError:
                        pass

                    type_ = get_type_as_str(arg_type)

            args.append(
                {
                    'name': arg.id,
                    'type': type_,
                    'message': ''
                })

        if node_type in ('method', 'classmethod'):
            try:
                args = args[1:]
            except IndexError:
                pass

        return \
            {
                'blocks':
                {
                    'Args': args,
                    'Raises': raises,
                    'Returns': returns,
                    'Warnings': warnings,
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
            previous_node = self.collector

        for node in (node for node in ast.walk(self.collector)
                     if isinstance(node, ast.FunctionDef)):
            if node.lineno >= row:
                return node
            previous_node = node

        # If we made it this far, assume that the row is within the last
        # element of this parse node
        #
        return previous_node or self.collector.body[-1]


def get_container_types():
    return \
        {
            ast.List: list,
            ast.Tuple: tuple,
            list: list,
            tuple: tuple,
        }


def get_type_as_str(object_type):
    def get_recursive_type(object_type):
        if type(object_type) in get_container_types():
            item_types = []
            for item in object_type:
                inner_item = get_type_as_str(item)
                if check.is_itertype(inner_item):
                    item_types.extend(inner_item)
                else:
                    item_types.append(inner_item)

            container_str = type(object_type).__name__
            if item_types:
                container_str += '[{types_}]'.format(
                    types_=', '.join(item_types))
            yield container_str
        else:
            yield object_type.__name__
    return list(get_recursive_type(object_type))[0]


def decompose_attribute(node):
    fields = [getattr(node, field) for field in node._fields]
    for index, field in enumerate(fields):
        if isinstance(field, ast.Name):
            fields[index] = [obj for obj in decompose_attribute(field)
                             if isinstance(obj, six.string_types)][0]

    return [name for name in fields if isinstance(name, six.string_types)]


def get_type_from_builtin_docstring(docstring):
    word_to_type = \
        {
            'list': list,
            'string': str,
            'strings': str,
        }

    # Usually something like 'S.split([sep [,maxsplit]]) -> list of strings'
    type_match_line = re.compile('^.+ -> (?P<return_type>.+)$')
    # Usually something like 'list' or 'list of strings'
    # expected_parse = pp.Word(pp.alphas) + \
    #     pp.ZeroOrMore(pp.White() + 'of' + pp.White() + pp.Word(pp.alphas))
    for line in docstring:
        match = type_match_line.match(line)
        if match is not None:
            return_types = [word for word in match.group('return_type').split(' of ')]
            # objects = expected_parse.parseString(match.group('return_type'))
            final_types = word_to_type[return_types[0]]
            if len(return_types) == 1:
                return final_types

            # Nest the types into one another. For example, ['list', 'str']
            # would be [str]. ['list', 'set', 'str'] would be [{str}]. Etc
            #
            final_types = final_types()
            previous_container = final_types
            for word in return_types[1:]:
                return_type = word_to_type[word]
                previous_container.append(return_type)
                previous_container = return_type
            return final_types
    raise RuntimeError('Return line was not found for docstring, "{doc}".'
                       ''.format(doc=docstring))


def get_container_from_type(obj):
    try:
        return get_container_types()[type(obj)]
    except KeyError:
        return list


def get_type(obj, parent=None):
    cast_python_types = get_type_from_ast(obj, parent=parent)
    if type(cast_python_types) == type or cast_python_types is None or \
            isinstance(cast_python_types, six.string_types):
        return cast_python_types
    elif callable(cast_python_types):
        # If it's some kind of function, just return it, as-is
        return cast_python_types.__name__

    unique_cast_objects = []
    for item in cast_python_types:
        if item not in unique_cast_objects:
            unique_cast_objects.append(item)

    final_cast_objects = cast_python_types.__class__(unique_cast_objects)
    return final_cast_objects


def locate(obj):
    stored_types = \
        {
            'join': str,
        }

    found_type = pydoc.locate(obj)
    if found_type is not None:
        return found_type

    try:
        return stored_types[obj]
    except KeyError:
        return


def get_function_call(obj):
    def get_recursive_id(obj):
        try:
            obj.value
        except AttributeError:
            yield obj.id
        else:
            for node in get_recursive_id(obj.value):
                yield node
            yield obj.attr

    return '.'.join(list(get_recursive_id(obj)))


def get_type_from_ast(obj, top_level=False, parent=None):
    def unpack_container_items(obj, parent=None):
        # elts is the elements in a container, like ast.List and ast.Tuple
        for field in obj.elts:
            try:
                if not field._fields:
                    raise ValueError('No fields were found for this object')
            except AttributeError:
                # This is probably a built-in type. If so, just return it
                yield type(field)
            except ValueError:
                pass
            else:
                yield get_type(field, parent=parent)

    try:
        return __builtin__.__dict__[type(obj).__name__]
    except KeyError:
        pass

    if isinstance(obj, ast.Attribute):
        obj = '.'.join(decompose_attribute(obj))
        return locate(obj)
    elif isinstance(obj, ast.Call):
        try:
            # Built-in functions like int() would match this, for example
            builtin_method = locate(obj.func.id)
            if builtin_method is not None:
                return builtin_method
        except AttributeError:
            pass

        try:
            function_value = obj.func.value
        except AttributeError:
            return obj.func.id

        if isinstance(function_value, (ast.Attribute, ast.Name)):
            cropped_obj = get_function_call(obj.func)

            # TODO : TBD should I remove this completely? Do I actually need a
            #        real function call or is the string name good enough?
            object_type = locate(cropped_obj)
            if object_type is None:
                return cropped_obj
            return object_type

        attribute_type = get_type_from_ast(function_value, top_level=True,
                                           parent=parent)
        if attribute_type.__name__ in __builtin__.__dict__:
            builtin_method = getattr(attribute_type(), obj.func.attr)

            strhelp = pydoc.render_doc(builtin_method)
            try:
                return get_type_from_builtin_docstring(strhelp.split('\n'))
            except RuntimeError:
                return

        return locate(obj)
    elif isinstance(obj, ast.Name):
        # Pretend the code is executable and try to get its type
        try:
            return type(ast.literal_eval(obj.id))
            # return get_type_as_str(type(eval(obj.id)))
        except ValueError:
            # The obj.id was likely not a built in type
            pass

        if parent is None:
            # raise NameError('Object: "{obj}" is not a built-in Python type. '
            #                 'No parent node was provided. Node type could not '
            #                 'be determined.'.format(obj=obj.id))
            return obj.id

        # If the object is defined locally, try to get its type and return it
        assign_object_type = None


        attribute_assign = None
        for assign_object in (node for node in ast.walk(parent)
                              if isinstance(node, ast.Assign)):
            for target in assign_object.targets:
                if hasattr(target, 'id') and target.id == obj.id:
                    for field in assign_object.value._fields:
                        field_obj = getattr(assign_object.value, field)
                        if not field_obj:
                            continue

                        if isinstance(field_obj, ast.Attribute):
                            try:
                                attribute_assign = ExitVisitor.types[field_obj.attr]
                            except KeyError:
                                pass

                        if attribute_assign is None:
                            try:
                                if isinstance(field_obj, list):
                                    # This is a dirty hack to unpack values that
                                    # sometimes get nested in a list when field
                                    # is some kind of iterable type, like generators
                                    #
                                    field_obj = field_obj[0]
                                assign_object_type = ExitVisitor.types[field_obj.__class__]
                            except KeyError:
                                pass

        assign_object_type = attribute_assign or assign_object_type
        if assign_object_type is not None:
            return assign_object_type
        return obj.id


    non_container_ast_types = \
        {
            ast.Num: int,
            ast.Str: str,
        }

    # Try to exit early if the type is generic enough
    try:
        return non_container_ast_types[type(obj)]
    except KeyError:
        pass

    # If we made it to this point, we should assume the object is a container
    # Example: a list or a tuple
    #
    # fields = [getattr(obj, field) for field in obj._fields]

    # flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]
    # fields = flatten(fields)

    cast_types = get_container_from_type(obj)

    if top_level:
        return cast_types

    # TODO : TBD does this need to be more generic?
    if isinstance(obj, ast.BinOp):
        fields = [getattr(obj.left, field) for field in obj.left._fields]
        return type(getattr(obj.left, obj.left._fields[0]))

    cast_types = cast_types(unpack_container_items(obj, parent=parent))
    return cast_types



if __name__ == '__main__':
    print(__doc__)

