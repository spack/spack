##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Enhanced YAML parsing for Spack.

- ``load()`` preserves YAML Marks on returned objects -- this allows
  us to access file and line information later.

- ``Our load methods use ``OrderedDict`` class instead of YAML's
  default unorderd dict.

"""
from ordereddict_backport import OrderedDict
from six import string_types, StringIO

import ruamel.yaml as yaml
from ruamel.yaml import Loader, Dumper
from ruamel.yaml.nodes import MappingNode, SequenceNode, ScalarNode
from ruamel.yaml.constructor import ConstructorError

from llnl.util.tty.color import colorize, clen, cextra

import spack.error

# Only export load and dump
__all__ = ['load', 'dump', 'SpackYAMLError']

# Make new classes so we can add custom attributes.
# Also, use OrderedDict instead of just dict.


class syaml_dict(OrderedDict):
    def __repr__(self):
        mappings = ('%r: %r' % (k, v) for k, v in self.items())
        return '{%s}' % ', '.join(mappings)


class syaml_list(list):
    __repr__ = list.__repr__


class syaml_str(str):
    __repr__ = str.__repr__


class syaml_int(int):
    __repr__ = str.__repr__


#: mapping from syaml type -> primitive type
syaml_types = {
    syaml_str: string_types,
    syaml_int: int,
    syaml_dict: dict,
    syaml_list: list,
}


def syaml_type(obj):
    """Get the corresponding syaml wrapper type for a primitive type.

    Return:
        (object): syaml-typed copy of object, or the obj if no wrapper
    """
    for syaml_t, t in syaml_types.items():
        if type(obj) is not bool and isinstance(obj, t):
            return syaml_t(obj) if type(obj) != syaml_t else obj
    return obj


def markable(obj):
    """Whether an object can be marked."""
    return type(obj) in syaml_types


def mark(obj, node):
    """Add start and end markers to an object."""
    if not markable(obj):
        return

    if hasattr(node, 'start_mark'):
        obj._start_mark = node.start_mark
    elif hasattr(node, '_start_mark'):
        obj._start_mark = node._start_mark

    if hasattr(node, 'end_mark'):
        obj._end_mark = node.end_mark
    elif hasattr(node, '_end_mark'):
        obj._end_mark = node._end_mark


def marked(obj):
    """Whether an object has been marked by spack_yaml."""
    return (hasattr(obj, '_start_mark') and obj._start_mark or
            hasattr(obj, '_end_mark') and obj._end_mark)


class OrderedLineLoader(Loader):
    """YAML loader that preserves order and line numbers.

       Mappings read in by this loader behave like an ordered dict.
       Sequences, mappings, and strings also have new attributes,
       ``_start_mark`` and ``_end_mark``, that preserve YAML line
       information in the output data.

    """
    #
    # Override construct_yaml_* so that they build our derived types,
    # which allows us to add new attributes to them.
    #
    # The standard YAML constructors return empty instances and fill
    # in with mappings later.  We preserve this behavior.
    #

    def construct_yaml_str(self, node):
        value = self.construct_scalar(node)
        value = syaml_str(value)
        mark(value, node)
        return value

    def construct_yaml_seq(self, node):
        data = syaml_list()
        mark(data, node)
        yield data
        data.extend(self.construct_sequence(node))

    def construct_yaml_map(self, node):
        data = syaml_dict()
        mark(data, node)
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    #
    # Override the ``construct_*`` routines. These fill in empty
    # objects after yielded by the above ``construct_yaml_*`` methods.
    #
    def construct_sequence(self, node, deep=False):
        if not isinstance(node, SequenceNode):
            raise ConstructorError(
                None, None,
                "expected a sequence node, but found %s" % node.id,
                node.start_mark)
        value = syaml_list(self.construct_object(child, deep=deep)
                           for child in node.value)
        mark(value, node)
        return value

    def construct_mapping(self, node, deep=False):
        """Store mappings as OrderedDicts instead of as regular python
           dictionaries to preserve file ordering."""
        if not isinstance(node, MappingNode):
            raise ConstructorError(
                None, None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark)

        mapping = syaml_dict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found unacceptable key (%s)" % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            if key in mapping:
                raise ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found already in-use key (%s)" % key, key_node.start_mark)
            mapping[key] = value

        mark(mapping, node)
        return mapping


# register above new constructors
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:map', OrderedLineLoader.construct_yaml_map)
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:seq', OrderedLineLoader.construct_yaml_seq)
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:str', OrderedLineLoader.construct_yaml_str)


class OrderedLineDumper(Dumper):
    """Dumper that preserves ordering and formats ``syaml_*`` objects.

      This dumper preserves insertion ordering ``syaml_dict`` objects
      when they're written out.  It also has some custom formatters
      for ``syaml_*`` objects so that they are formatted like their
      regular Python equivalents, instead of ugly YAML pyobjects.

    """

    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        node = MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            # if it's a syaml_dict, preserve OrderedDict order.
            # Otherwise do the default thing.
            sort = not isinstance(mapping, syaml_dict)
            mapping = list(mapping.items())
            if sort:
                mapping.sort()

        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and
                    not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style

        return node

    def ignore_aliases(self, _data):
        """Make the dumper NEVER print YAML aliases."""
        return True


# Make our special objects look like normal YAML ones.
OrderedLineDumper.add_representer(syaml_dict, OrderedLineDumper.represent_dict)
OrderedLineDumper.add_representer(syaml_list, OrderedLineDumper.represent_list)
OrderedLineDumper.add_representer(syaml_str, OrderedLineDumper.represent_str)
OrderedLineDumper.add_representer(syaml_int, OrderedLineDumper.represent_int)


def file_line(mark):
    """Format a mark as <file>:<line> information."""
    result = mark.name
    if mark.line:
        result += ':' + str(mark.line)
    return result


#: Global for interactions between LineAnnotationDumper and dump_annotated().
#: This is nasty but YAML doesn't give us many ways to pass arguments --
#: yaml.dump() takes a class (not an instance) and instantiates the dumper
#: itself, so we can't just pass an instance
_annotations = []


class LineAnnotationDumper(OrderedLineDumper):
    """Dumper that generates per-line annotations.

    Annotations are stored in the ``_annotations`` global.  After one
    dump pass, the strings in ``_annotations`` will correspond one-to-one
    with the lines output by the dumper.

    LineAnnotationDumper records blame information after each line is
    generated. As each line is parsed, it saves file/line info for each
    object printed. At the end of each line, it creates an annotation
    based on the saved mark and stores it in ``_annotations``.

    For an example of how to use this, see ``dump_annotated()``, which
    writes to a ``StringIO`` then joins the lines from that with
    annotations.
    """
    saved = None

    def __init__(self, *args, **kwargs):
        super(LineAnnotationDumper, self).__init__(*args, **kwargs)
        del _annotations[:]

    def process_scalar(self):
        super(LineAnnotationDumper, self).process_scalar()
        if marked(self.event.value):
            self.saved = self.event.value

    def represent_data(self, data):
        """Force syaml_str to be passed through with marks."""
        result = super(LineAnnotationDumper, self).represent_data(data)
        if isinstance(result.value, string_types):
            result.value = syaml_str(data)
        mark(result.value, data)
        return result

    def write_stream_start(self):
        super(LineAnnotationDumper, self).write_stream_start()
        _annotations.append(colorize('@K{---}'))

    def write_line_break(self):
        super(LineAnnotationDumper, self).write_line_break()
        if not self.saved:
            return

        # append annotations at the end of each line
        if self.saved:
            mark = self.saved._start_mark
            ann = '@K{%s}' % mark.name
            if mark.line is not None:
                ann += ':@c{%s}' % (mark.line + 1)
            _annotations.append(colorize(ann))
        else:
            _annotations.append('')


def load(*args, **kwargs):
    """Load but modify the loader instance so that it will add __line__
       atrributes to the returned object."""
    kwargs['Loader'] = OrderedLineLoader
    return yaml.load(*args, **kwargs)


def dump(*args, **kwargs):
    blame = kwargs.pop('blame', False)

    if blame:
        return dump_annotated(*args, **kwargs)
    else:
        kwargs['Dumper'] = OrderedLineDumper
        return yaml.dump(*args, **kwargs)


def dump_annotated(data, stream=None, *args, **kwargs):
    kwargs['Dumper'] = LineAnnotationDumper

    sio = StringIO()
    yaml.dump(data, sio, *args, **kwargs)
    lines = sio.getvalue().rstrip().split('\n')

    getvalue = None
    if stream is None:
        stream = StringIO()
        getvalue = stream.getvalue

    # write out annotations and linees, accounting for color
    width = max(clen(a) for a in _annotations)
    formats = ['%%-%ds  %%s\n' % (width + cextra(a)) for a in _annotations]

    for f, a, l in zip(formats, _annotations, lines):
        stream.write(f % (a, l))

    if getvalue:
        return getvalue()


class SpackYAMLError(spack.error.SpackError):
    """Raised when there are issues with YAML parsing."""
    def __init__(self, msg, yaml_error):
        super(SpackYAMLError, self).__init__(msg, str(yaml_error))
