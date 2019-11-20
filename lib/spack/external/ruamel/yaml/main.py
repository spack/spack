# coding: utf-8

from __future__ import absolute_import


from ruamel.yaml.error import *                                # NOQA

from ruamel.yaml.tokens import *                               # NOQA
from ruamel.yaml.events import *                               # NOQA
from ruamel.yaml.nodes import *                                # NOQA

from ruamel.yaml.loader import *                               # NOQA
from ruamel.yaml.dumper import *                               # NOQA
from ruamel.yaml.compat import StringIO, BytesIO, with_metaclass, PY3

# import io


def scan(stream, Loader=Loader):
    """
    Scan a YAML stream and produce scanning tokens.
    """
    loader = Loader(stream)
    try:
        while loader.check_token():
            yield loader.get_token()
    finally:
        loader.dispose()


def parse(stream, Loader=Loader):
    """
    Parse a YAML stream and produce parsing events.
    """
    loader = Loader(stream)
    try:
        while loader.check_event():
            yield loader.get_event()
    finally:
        loader.dispose()


def compose(stream, Loader=Loader):
    """
    Parse the first YAML document in a stream
    and produce the corresponding representation tree.
    """
    loader = Loader(stream)
    try:
        return loader.get_single_node()
    finally:
        loader.dispose()


def compose_all(stream, Loader=Loader):
    """
    Parse all YAML documents in a stream
    and produce corresponding representation trees.
    """
    loader = Loader(stream)
    try:
        while loader.check_node():
            yield loader.get_node()
    finally:
        loader.dispose()


def load(stream, Loader=Loader, version=None, preserve_quotes=None):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    loader = Loader(stream, version, preserve_quotes=preserve_quotes)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()


def load_all(stream, Loader=Loader, version=None):
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """
    loader = Loader(stream, version)
    try:
        while loader.check_data():
            yield loader.get_data()
    finally:
        loader.dispose()


def safe_load(stream, version=None):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    Resolve only basic YAML tags.
    """
    return load(stream, SafeLoader, version)


def safe_load_all(stream, version=None):
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    Resolve only basic YAML tags.
    """
    return load_all(stream, SafeLoader, version)


def round_trip_load(stream, version=None, preserve_quotes=None):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    Resolve only basic YAML tags.
    """
    return load(stream, RoundTripLoader, version, preserve_quotes=preserve_quotes)


def round_trip_load_all(stream, version=None, preserve_quotes=None):
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    Resolve only basic YAML tags.
    """
    return load_all(stream, RoundTripLoader, version, preserve_quotes=preserve_quotes)


def emit(events, stream=None, Dumper=Dumper,
         canonical=None, indent=None, width=None,
         allow_unicode=None, line_break=None):
    """
    Emit YAML parsing events into a stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if stream is None:
        stream = StringIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break)
    try:
        for event in events:
            dumper.emit(event)
    finally:
        dumper.dispose()
    if getvalue:
        return getvalue()

enc = None if PY3 else 'utf-8'


def serialize_all(nodes, stream=None, Dumper=Dumper,
                  canonical=None, indent=None, width=None,
                  allow_unicode=None, line_break=None,
                  encoding=enc, explicit_start=None, explicit_end=None,
                  version=None, tags=None):
    """
    Serialize a sequence of representation trees into a YAML stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if stream is None:
        if encoding is None:
            stream = StringIO()
        else:
            stream = BytesIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break,
                    encoding=encoding, version=version, tags=tags,
                    explicit_start=explicit_start, explicit_end=explicit_end)
    try:
        dumper.open()
        for node in nodes:
            dumper.serialize(node)
        dumper.close()
    finally:
        dumper.dispose()
    if getvalue:
        return getvalue()


def serialize(node, stream=None, Dumper=Dumper, **kwds):
    """
    Serialize a representation tree into a YAML stream.
    If stream is None, return the produced string instead.
    """
    return serialize_all([node], stream, Dumper=Dumper, **kwds)


def dump_all(documents, stream=None, Dumper=Dumper,
             default_style=None, default_flow_style=None,
             canonical=None, indent=None, width=None,
             allow_unicode=None, line_break=None,
             encoding=enc, explicit_start=None, explicit_end=None,
             version=None, tags=None, block_seq_indent=None,
             top_level_colon_align=None, prefix_colon=None):
    """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if top_level_colon_align is True:
        top_level_colon_align = max([len(str(x)) for x in documents[0]])
    if stream is None:
        if encoding is None:
            stream = StringIO()
        else:
            stream = BytesIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end, version=version,
                    tags=tags, block_seq_indent=block_seq_indent,
                    top_level_colon_align=top_level_colon_align, prefix_colon=prefix_colon,
                    )
    try:
        dumper.open()
        for data in documents:
            dumper.represent(data)
        dumper.close()
    finally:
        dumper.dispose()
    if getvalue:
        return getvalue()


def dump(data, stream=None, Dumper=Dumper,
         default_style=None, default_flow_style=None,
         canonical=None, indent=None, width=None,
         allow_unicode=None, line_break=None,
         encoding=enc, explicit_start=None, explicit_end=None,
         version=None, tags=None, block_seq_indent=None):
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.

    default_style ∈ None, '', '"', "'", '|', '>'

    """
    return dump_all([data], stream, Dumper=Dumper,
                    default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical,
                    indent=indent, width=width,
                    allow_unicode=allow_unicode,
                    line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end,
                    version=version, tags=tags, block_seq_indent=block_seq_indent)


def safe_dump_all(documents, stream=None, **kwds):
    """
    Serialize a sequence of Python objects into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
    return dump_all(documents, stream, Dumper=SafeDumper, **kwds)


def safe_dump(data, stream=None, **kwds):
    """
    Serialize a Python object into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
    return dump_all([data], stream, Dumper=SafeDumper, **kwds)


def round_trip_dump(data, stream=None, Dumper=RoundTripDumper,
                    default_style=None, default_flow_style=None,
                    canonical=None, indent=None, width=None,
                    allow_unicode=None, line_break=None,
                    encoding=enc, explicit_start=None, explicit_end=None,
                    version=None, tags=None, block_seq_indent=None,
                    top_level_colon_align=None, prefix_colon=None):
    allow_unicode = True if allow_unicode is None else allow_unicode
    return dump_all([data], stream, Dumper=Dumper,
                    default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical,
                    indent=indent, width=width,
                    allow_unicode=allow_unicode,
                    line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end,
                    version=version, tags=tags, block_seq_indent=block_seq_indent,
                    top_level_colon_align=top_level_colon_align, prefix_colon=prefix_colon)


def add_implicit_resolver(tag, regexp, first=None,
                          Loader=Loader, Dumper=Dumper):
    """
    Add an implicit scalar detector.
    If an implicit scalar value matches the given regexp,
    the corresponding tag is assigned to the scalar.
    first is a sequence of possible initial characters or None.
    """
    Loader.add_implicit_resolver(tag, regexp, first)
    Dumper.add_implicit_resolver(tag, regexp, first)


def add_path_resolver(tag, path, kind=None, Loader=Loader, Dumper=Dumper):
    """
    Add a path based resolver for the given tag.
    A path is a list of keys that forms a path
    to a node in the representation tree.
    Keys can be string values, integers, or None.
    """
    Loader.add_path_resolver(tag, path, kind)
    Dumper.add_path_resolver(tag, path, kind)


def add_constructor(tag, constructor, Loader=Loader):
    """
    Add a constructor for the given tag.
    Constructor is a function that accepts a Loader instance
    and a node object and produces the corresponding Python object.
    """
    Loader.add_constructor(tag, constructor)


def add_multi_constructor(tag_prefix, multi_constructor, Loader=Loader):
    """
    Add a multi-constructor for the given tag prefix.
    Multi-constructor is called for a node if its tag starts with tag_prefix.
    Multi-constructor accepts a Loader instance, a tag suffix,
    and a node object and produces the corresponding Python object.
    """
    Loader.add_multi_constructor(tag_prefix, multi_constructor)


def add_representer(data_type, representer, Dumper=Dumper):
    """
    Add a representer for the given type.
    Representer is a function accepting a Dumper instance
    and an instance of the given data type
    and producing the corresponding representation node.
    """
    Dumper.add_representer(data_type, representer)


def add_multi_representer(data_type, multi_representer, Dumper=Dumper):
    """
    Add a representer for the given type.
    Multi-representer is a function accepting a Dumper instance
    and an instance of the given data type or subtype
    and producing the corresponding representation node.
    """
    Dumper.add_multi_representer(data_type, multi_representer)


class YAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """
    def __init__(cls, name, bases, kwds):
        super(YAMLObjectMetaclass, cls).__init__(name, bases, kwds)
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
            cls.yaml_dumper.add_representer(cls, cls.to_yaml)


class YAMLObject(with_metaclass(YAMLObjectMetaclass)):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """
    __slots__ = ()  # no direct instantiation, so allow immutable subclasses

    yaml_loader = Loader
    yaml_dumper = Dumper

    yaml_tag = None
    yaml_flow_style = None

    @classmethod
    def from_yaml(cls, loader, node):
        """
        Convert a representation node to a Python object.
        """
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, dumper, data):
        """
        Convert a Python object to a representation node.
        """
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls,
                                            flow_style=cls.yaml_flow_style)
