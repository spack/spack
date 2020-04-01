# coding: utf-8

from __future__ import absolute_import

import re

try:
    from .error import *                               # NOQA
    from .nodes import *                               # NOQA
    from .compat import string_types
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.error import *                               # NOQA
    from ruamel.yaml.nodes import *                               # NOQA
    from ruamel.yaml.compat import string_types

__all__ = ['BaseResolver', 'Resolver', 'VersionedResolver']


_DEFAULT_VERSION = (1, 2)


class ResolverError(YAMLError):
    pass


class BaseResolver(object):

    DEFAULT_SCALAR_TAG = u'tag:yaml.org,2002:str'
    DEFAULT_SEQUENCE_TAG = u'tag:yaml.org,2002:seq'
    DEFAULT_MAPPING_TAG = u'tag:yaml.org,2002:map'

    yaml_implicit_resolvers = {}
    yaml_path_resolvers = {}

    def __init__(self):
        self._loader_version = None
        self.resolver_exact_paths = []
        self.resolver_prefix_paths = []

    @classmethod
    def add_implicit_resolver(cls, tag, regexp, first):
        if 'yaml_implicit_resolvers' not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()
        if first is None:
            first = [None]
        for ch in first:
            cls.yaml_implicit_resolvers.setdefault(ch, []).append(
                (tag, regexp))

    @classmethod
    def add_path_resolver(cls, tag, path, kind=None):
        # Note: `add_path_resolver` is experimental.  The API could be changed.
        # `new_path` is a pattern that is matched against the path from the
        # root to the node that is being considered.  `node_path` elements are
        # tuples `(node_check, index_check)`.  `node_check` is a node class:
        # `ScalarNode`, `SequenceNode`, `MappingNode` or `None`.  `None`
        # matches any kind of a node.  `index_check` could be `None`, a boolean
        # value, a string value, or a number.  `None` and `False` match against
        # any _value_ of sequence and mapping nodes.  `True` matches against
        # any _key_ of a mapping node.  A string `index_check` matches against
        # a mapping value that corresponds to a scalar key which content is
        # equal to the `index_check` value.  An integer `index_check` matches
        # against a sequence value with the index equal to `index_check`.
        if 'yaml_path_resolvers' not in cls.__dict__:
            cls.yaml_path_resolvers = cls.yaml_path_resolvers.copy()
        new_path = []
        for element in path:
            if isinstance(element, (list, tuple)):
                if len(element) == 2:
                    node_check, index_check = element
                elif len(element) == 1:
                    node_check = element[0]
                    index_check = True
                else:
                    raise ResolverError("Invalid path element: %s" % element)
            else:
                node_check = None
                index_check = element
            if node_check is str:
                node_check = ScalarNode
            elif node_check is list:
                node_check = SequenceNode
            elif node_check is dict:
                node_check = MappingNode
            elif node_check not in [ScalarNode, SequenceNode, MappingNode]  \
                    and not isinstance(node_check, string_types)  \
                    and node_check is not None:
                raise ResolverError("Invalid node checker: %s" % node_check)
            if not isinstance(index_check, (string_types, int))   \
                    and index_check is not None:
                raise ResolverError("Invalid index checker: %s" % index_check)
            new_path.append((node_check, index_check))
        if kind is str:
            kind = ScalarNode
        elif kind is list:
            kind = SequenceNode
        elif kind is dict:
            kind = MappingNode
        elif kind not in [ScalarNode, SequenceNode, MappingNode]    \
                and kind is not None:
            raise ResolverError("Invalid node kind: %s" % kind)
        cls.yaml_path_resolvers[tuple(new_path), kind] = tag

    def descend_resolver(self, current_node, current_index):
        if not self.yaml_path_resolvers:
            return
        exact_paths = {}
        prefix_paths = []
        if current_node:
            depth = len(self.resolver_prefix_paths)
            for path, kind in self.resolver_prefix_paths[-1]:
                if self.check_resolver_prefix(depth, path, kind,
                                              current_node, current_index):
                    if len(path) > depth:
                        prefix_paths.append((path, kind))
                    else:
                        exact_paths[kind] = self.yaml_path_resolvers[path,
                                                                     kind]
        else:
            for path, kind in self.yaml_path_resolvers:
                if not path:
                    exact_paths[kind] = self.yaml_path_resolvers[path, kind]
                else:
                    prefix_paths.append((path, kind))
        self.resolver_exact_paths.append(exact_paths)
        self.resolver_prefix_paths.append(prefix_paths)

    def ascend_resolver(self):
        if not self.yaml_path_resolvers:
            return
        self.resolver_exact_paths.pop()
        self.resolver_prefix_paths.pop()

    def check_resolver_prefix(self, depth, path, kind,
                              current_node, current_index):
        node_check, index_check = path[depth-1]
        if isinstance(node_check, string_types):
            if current_node.tag != node_check:
                return
        elif node_check is not None:
            if not isinstance(current_node, node_check):
                return
        if index_check is True and current_index is not None:
            return
        if (index_check is False or index_check is None)    \
                and current_index is None:
            return
        if isinstance(index_check, string_types):
            if not (isinstance(current_index, ScalarNode) and
                    index_check == current_index.value):
                return
        elif isinstance(index_check, int) and not isinstance(index_check,
                                                             bool):
            if index_check != current_index:
                return
        return True

    def resolve(self, kind, value, implicit):
        if kind is ScalarNode and implicit[0]:
            if value == u'':
                resolvers = self.yaml_implicit_resolvers.get(u'', [])
            else:
                resolvers = self.yaml_implicit_resolvers.get(value[0], [])
            resolvers += self.yaml_implicit_resolvers.get(None, [])
            for tag, regexp in resolvers:
                if regexp.match(value):
                    return tag
            implicit = implicit[1]
        if self.yaml_path_resolvers:
            exact_paths = self.resolver_exact_paths[-1]
            if kind in exact_paths:
                return exact_paths[kind]
            if None in exact_paths:
                return exact_paths[None]
        if kind is ScalarNode:
            return self.DEFAULT_SCALAR_TAG
        elif kind is SequenceNode:
            return self.DEFAULT_SEQUENCE_TAG
        elif kind is MappingNode:
            return self.DEFAULT_MAPPING_TAG

    @property
    def processing_version(self):
        return None


class Resolver(BaseResolver):
    pass

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:bool',
    re.compile(u'''^(?:yes|Yes|YES|no|No|NO
    |true|True|TRUE|false|False|FALSE
    |on|On|ON|off|Off|OFF)$''', re.X),
    list(u'yYnNtTfFoO'))

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:int',
    re.compile(u'''^(?:[-+]?0b[0-1_]+
    |[-+]?0o?[0-7_]+
    |[-+]?(?:0|[1-9][0-9_]*)
    |[-+]?0x[0-9a-fA-F_]+
    |[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$''', re.X),
    list(u'-+0123456789'))

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:merge',
    re.compile(u'^(?:<<)$'),
    [u'<'])

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:null',
    re.compile(u'''^(?: ~
    |null|Null|NULL
    | )$''', re.X),
    [u'~', u'n', u'N', u''])

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:timestamp',
    re.compile(u'''^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]
    |[0-9][0-9][0-9][0-9] -[0-9][0-9]? -[0-9][0-9]?
    (?:[Tt]|[ \\t]+)[0-9][0-9]?
    :[0-9][0-9] :[0-9][0-9] (?:\\.[0-9]*)?
    (?:[ \\t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)$''', re.X),
    list(u'0123456789'))

Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:value',
    re.compile(u'^(?:=)$'),
    [u'='])

# The following resolver is only for documentation purposes. It cannot work
# because plain scalars cannot start with '!', '&', or '*'.
Resolver.add_implicit_resolver(
    u'tag:yaml.org,2002:yaml',
    re.compile(u'^(?:!|&|\\*)$'),
    list(u'!&*'))

# resolvers consist of
# - a list of applicable version
# - a tag
# - a regexp
# - a list of first characters to match
implicit_resolvers = [
    ([(1, 2)],
        u'tag:yaml.org,2002:bool',
        re.compile(u'''^(?:true|True|TRUE|false|False|FALSE)$''', re.X),
        list(u'tTfF')),
    ([(1, 1)],
        u'tag:yaml.org,2002:bool',
        re.compile(u'''^(?:yes|Yes|YES|no|No|NO
        |true|True|TRUE|false|False|FALSE
        |on|On|ON|off|Off|OFF)$''', re.X),
        list(u'yYnNtTfFoO')),
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:float',
        re.compile(u'''^(?:
         [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$''', re.X),
        list(u'-+0123456789.')),
    ([(1, 2)],
        u'tag:yaml.org,2002:int',
        re.compile(u'''^(?:[-+]?0b[0-1_]+
        |[-+]?0o?[0-7_]+
        |[-+]?(?:0|[1-9][0-9_]*)
        |[-+]?0x[0-9a-fA-F_]+)$''', re.X),
        list(u'-+0123456789')),
    ([(1, 1)],
        u'tag:yaml.org,2002:int',
        re.compile(u'''^(?:[-+]?0b[0-1_]+
        |[-+]?0o?[0-7_]+
        |[-+]?(?:0|[1-9][0-9_]*)
        |[-+]?0x[0-9a-fA-F_]+
        |[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$''', re.X),
        list(u'-+0123456789')),
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:merge',
        re.compile(u'^(?:<<)$'),
        [u'<']),
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:null',
        re.compile(u'''^(?: ~
        |null|Null|NULL
        | )$''', re.X),
        [u'~', u'n', u'N', u'']),
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:timestamp',
        re.compile(u'''^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]
        |[0-9][0-9][0-9][0-9] -[0-9][0-9]? -[0-9][0-9]?
        (?:[Tt]|[ \\t]+)[0-9][0-9]?
        :[0-9][0-9] :[0-9][0-9] (?:\\.[0-9]*)?
        (?:[ \\t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)$''', re.X),
        list(u'0123456789')),
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:value',
        re.compile(u'^(?:=)$'),
        [u'=']),
    # The following resolver is only for documentation purposes. It cannot work
    # because plain scalars cannot start with '!', '&', or '*'.
    ([(1, 2), (1, 1)],
        u'tag:yaml.org,2002:yaml',
        re.compile(u'^(?:!|&|\\*)$'),
        list(u'!&*')),
]


class VersionedResolver(BaseResolver):
    """
    contrary to the "normal" resolver, the smart resolver delays loading
    the pattern matching rules. That way it can decide to load 1.1 rules
    or the (default) 1.2 that no longer support octal without 0o, sexagesimals
    and Yes/No/On/Off booleans.
    """

    def __init__(self, version=None):
        BaseResolver.__init__(self)
        self._loader_version = self.get_loader_version(version)
        self._version_implicit_resolver = {}

    def add_version_implicit_resolver(self, version, tag, regexp, first):
        if first is None:
            first = [None]
        impl_resolver = self._version_implicit_resolver.setdefault(version, {})
        for ch in first:
            impl_resolver.setdefault(ch, []).append((tag, regexp))

    def get_loader_version(self, version):
        if version is None or isinstance(version, tuple):
            return version
        if isinstance(version, list):
            return tuple(version)
        # assume string
        return tuple(map(int, version.split(u'.')))

    @property
    def resolver(self):
        """
        select the resolver based on the version we are parsing
        """
        version = self.processing_version
        if version not in self._version_implicit_resolver:
            for x in implicit_resolvers:
                if version in x[0]:
                    self.add_version_implicit_resolver(version, x[1], x[2], x[3])
        return self._version_implicit_resolver[version]

    def resolve(self, kind, value, implicit):
        if kind is ScalarNode and implicit[0]:
            if value == u'':
                resolvers = self.resolver.get(u'', [])
            else:
                resolvers = self.resolver.get(value[0], [])
            resolvers += self.resolver.get(None, [])
            for tag, regexp in resolvers:
                if regexp.match(value):
                    return tag
            implicit = implicit[1]
        if self.yaml_path_resolvers:
            exact_paths = self.resolver_exact_paths[-1]
            if kind in exact_paths:
                return exact_paths[kind]
            if None in exact_paths:
                return exact_paths[None]
        if kind is ScalarNode:
            return self.DEFAULT_SCALAR_TAG
        elif kind is SequenceNode:
            return self.DEFAULT_SEQUENCE_TAG
        elif kind is MappingNode:
            return self.DEFAULT_MAPPING_TAG

    @property
    def processing_version(self):
        try:
            version = self.yaml_version
        except AttributeError:
            # dumping
            version = self.use_version
        if version is None:
            version = self._loader_version
            if version is None:
                version = _DEFAULT_VERSION
        return version
