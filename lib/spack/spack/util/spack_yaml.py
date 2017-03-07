##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import yaml
from yaml import Loader, Dumper
from yaml.nodes import *
from yaml.constructor import ConstructorError
from ordereddict_backport import OrderedDict

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


def mark(obj, node):
    """Add start and end markers to an object."""
    obj._start_mark = node.start_mark
    obj._end_mark = node.end_mark


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
    u'tag:yaml.org,2002:map', OrderedLineLoader.construct_yaml_map)
OrderedLineLoader.add_constructor(
    u'tag:yaml.org,2002:seq', OrderedLineLoader.construct_yaml_seq)
OrderedLineLoader.add_constructor(
    u'tag:yaml.org,2002:str', OrderedLineLoader.construct_yaml_str)


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


def load(*args, **kwargs):
    """Load but modify the loader instance so that it will add __line__
       atrributes to the returned object."""
    kwargs['Loader'] = OrderedLineLoader
    return yaml.load(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs['Dumper'] = OrderedLineDumper
    return yaml.dump(*args, **kwargs)


class SpackYAMLError(spack.error.SpackError):
    """Raised when there are issues with YAML parsing."""
    def __init__(self, msg, yaml_error):
        super(SpackYAMLError, self).__init__(msg, str(yaml_error))
