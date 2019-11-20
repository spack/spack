# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

try:
    from .error import *                                  # NOQA
    from .nodes import *                                  # NOQA
    from .compat import text_type, binary_type, to_unicode, PY2, PY3, ordereddict
    from .scalarstring import *                           # NOQA
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.error import *                       # NOQA
    from ruamel.yaml.nodes import *                       # NOQA
    from ruamel.yaml.compat import text_type, binary_type, to_unicode, PY2, PY3, ordereddict
    from ruamel.yaml.scalarstring import *                # NOQA


import datetime
import sys
import types
if PY3:
    import copyreg
    import base64
else:
    import copy_reg as copyreg


__all__ = ['BaseRepresenter', 'SafeRepresenter', 'Representer',
           'RepresenterError', 'RoundTripRepresenter']


class RepresenterError(YAMLError):
    pass


class BaseRepresenter(object):

    yaml_representers = {}
    yaml_multi_representers = {}

    def __init__(self, default_style=None, default_flow_style=None):
        self.default_style = default_style
        self.default_flow_style = default_flow_style
        self.represented_objects = {}
        self.object_keeper = []
        self.alias_key = None

    def represent(self, data):
        node = self.represent_data(data)
        self.serialize(node)
        self.represented_objects = {}
        self.object_keeper = []
        self.alias_key = None

    if PY2:
        def get_classobj_bases(self, cls):
            bases = [cls]
            for base in cls.__bases__:
                bases.extend(self.get_classobj_bases(base))
            return bases

    def represent_data(self, data):
        if self.ignore_aliases(data):
            self.alias_key = None
        else:
            self.alias_key = id(data)
        if self.alias_key is not None:
            if self.alias_key in self.represented_objects:
                node = self.represented_objects[self.alias_key]
                # if node is None:
                #     raise RepresenterError(
                #          "recursive objects are not allowed: %r" % data)
                return node
            # self.represented_objects[alias_key] = None
            self.object_keeper.append(data)
        data_types = type(data).__mro__
        if PY2:
            # if type(data) is types.InstanceType:
            if isinstance(data, types.InstanceType):
                data_types = self.get_classobj_bases(data.__class__) + \
                    list(data_types)
        if data_types[0] in self.yaml_representers:
            node = self.yaml_representers[data_types[0]](self, data)
        else:
            for data_type in data_types:
                if data_type in self.yaml_multi_representers:
                    node = self.yaml_multi_representers[data_type](self, data)
                    break
            else:
                if None in self.yaml_multi_representers:
                    node = self.yaml_multi_representers[None](self, data)
                elif None in self.yaml_representers:
                    node = self.yaml_representers[None](self, data)
                else:
                    node = ScalarNode(None, text_type(data))
        # if alias_key is not None:
        #     self.represented_objects[alias_key] = node
        return node

    def represent_key(self, data):
        """
        David Fraser: Extract a method to represent keys in mappings, so that
        a subclass can choose not to quote them (for example)
        used in repesent_mapping
        https://bitbucket.org/davidfraser/pyyaml/commits/d81df6eb95f20cac4a79eed95ae553b5c6f77b8c
        """
        return self.represent_data(data)

    @classmethod
    def add_representer(cls, data_type, representer):
        if 'yaml_representers' not in cls.__dict__:
            cls.yaml_representers = cls.yaml_representers.copy()
        cls.yaml_representers[data_type] = representer

    @classmethod
    def add_multi_representer(cls, data_type, representer):
        if 'yaml_multi_representers' not in cls.__dict__:
            cls.yaml_multi_representers = cls.yaml_multi_representers.copy()
        cls.yaml_multi_representers[data_type] = representer

    def represent_scalar(self, tag, value, style=None):
        if style is None:
            style = self.default_style
        node = ScalarNode(tag, value, style=style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        return node

    def represent_sequence(self, tag, sequence, flow_style=None):
        value = []
        node = SequenceNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        for item in sequence:
            node_item = self.represent_data(item)
            if not (isinstance(node_item, ScalarNode) and not node_item.style):
                best_style = False
            value.append(node_item)
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_omap(self, tag, omap, flow_style=None):
        value = []
        node = SequenceNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        for item_key in omap:
            item_val = omap[item_key]
            node_item = self.represent_data({item_key: item_val})
            # if not (isinstance(node_item, ScalarNode) \
            #    and not node_item.style):
            #     best_style = False
            value.append(node_item)
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        node = MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            mapping = list(mapping.items())
            try:
                mapping = sorted(mapping)
            except TypeError:
                pass
        for item_key, item_value in mapping:
            node_key = self.represent_key(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and not
                    node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def ignore_aliases(self, data):
        return False


class SafeRepresenter(BaseRepresenter):

    def ignore_aliases(self, data):
        # https://docs.python.org/3/reference/expressions.html#parenthesized-forms :
        # "i.e. two occurrences of the empty tuple may or may not yield the same object"
        # so "data is ()" should not be used
        if data is None or data == ():
            return True
        if isinstance(data, (binary_type, text_type, bool, int, float)):
            return True

    def represent_none(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:null',
                                     u'null')

    if PY3:
        def represent_str(self, data):
            return self.represent_scalar(u'tag:yaml.org,2002:str', data)

        def represent_binary(self, data):
            if hasattr(base64, 'encodebytes'):
                data = base64.encodebytes(data).decode('ascii')
            else:
                data = base64.encodestring(data).decode('ascii')
            return self.represent_scalar(u'tag:yaml.org,2002:binary', data,
                                         style='|')
    else:
        def represent_str(self, data):
            tag = None
            style = None
            try:
                data = unicode(data, 'ascii')
                tag = u'tag:yaml.org,2002:str'
            except UnicodeDecodeError:
                try:
                    data = unicode(data, 'utf-8')
                    tag = u'tag:yaml.org,2002:str'
                except UnicodeDecodeError:
                    data = data.encode('base64')
                    tag = u'tag:yaml.org,2002:binary'
                    style = '|'
            return self.represent_scalar(tag, data, style=style)

        def represent_unicode(self, data):
            return self.represent_scalar(u'tag:yaml.org,2002:str', data)

    def represent_bool(self, data):
        if data:
            value = u'true'
        else:
            value = u'false'
        return self.represent_scalar(u'tag:yaml.org,2002:bool', value)

    def represent_int(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:int', text_type(data))

    if PY2:
        def represent_long(self, data):
            return self.represent_scalar(u'tag:yaml.org,2002:int',
                                         text_type(data))

    inf_value = 1e300
    while repr(inf_value) != repr(inf_value*inf_value):
        inf_value *= inf_value

    def represent_float(self, data):
        if data != data or (data == 0.0 and data == 1.0):
            value = u'.nan'
        elif data == self.inf_value:
            value = u'.inf'
        elif data == -self.inf_value:
            value = u'-.inf'
        else:
            value = to_unicode(repr(data)).lower()
            # Note that in some cases `repr(data)` represents a float number
            # without the decimal parts.  For instance:
            #   >>> repr(1e17)
            #   '1e17'
            # Unfortunately, this is not a valid float representation according
            # to the definition of the `!!float` tag.  We fix this by adding
            # '.0' before the 'e' symbol.
            if u'.' not in value and u'e' in value:
                value = value.replace(u'e', u'.0e', 1)
        return self.represent_scalar(u'tag:yaml.org,2002:float', value)

    def represent_list(self, data):
        # pairs = (len(data) > 0 and isinstance(data, list))
        # if pairs:
        #     for item in data:
        #         if not isinstance(item, tuple) or len(item) != 2:
        #             pairs = False
        #             break
        # if not pairs:
            return self.represent_sequence(u'tag:yaml.org,2002:seq', data)
        # value = []
        # for item_key, item_value in data:
        #     value.append(self.represent_mapping(u'tag:yaml.org,2002:map',
        #         [(item_key, item_value)]))
        # return SequenceNode(u'tag:yaml.org,2002:pairs', value)

    def represent_dict(self, data):
        return self.represent_mapping(u'tag:yaml.org,2002:map', data)

    def represent_ordereddict(self, data):
        return self.represent_omap(u'tag:yaml.org,2002:omap', data)

    def represent_set(self, data):
        value = {}
        for key in data:
            value[key] = None
        return self.represent_mapping(u'tag:yaml.org,2002:set', value)

    def represent_date(self, data):
        value = to_unicode(data.isoformat())
        return self.represent_scalar(u'tag:yaml.org,2002:timestamp', value)

    def represent_datetime(self, data):
        value = to_unicode(data.isoformat(' '))
        return self.represent_scalar(u'tag:yaml.org,2002:timestamp', value)

    def represent_yaml_object(self, tag, data, cls, flow_style=None):
        if hasattr(data, '__getstate__'):
            state = data.__getstate__()
        else:
            state = data.__dict__.copy()
        return self.represent_mapping(tag, state, flow_style=flow_style)

    def represent_undefined(self, data):
        raise RepresenterError("cannot represent an object: %s" % data)

SafeRepresenter.add_representer(type(None),
                                SafeRepresenter.represent_none)

SafeRepresenter.add_representer(str,
                                SafeRepresenter.represent_str)

if PY2:
    SafeRepresenter.add_representer(unicode,
                                    SafeRepresenter.represent_unicode)
else:
    SafeRepresenter.add_representer(bytes,
                                    SafeRepresenter.represent_binary)

SafeRepresenter.add_representer(bool,
                                SafeRepresenter.represent_bool)

SafeRepresenter.add_representer(int,
                                SafeRepresenter.represent_int)

if PY2:
    SafeRepresenter.add_representer(long,
                                    SafeRepresenter.represent_long)

SafeRepresenter.add_representer(float,
                                SafeRepresenter.represent_float)

SafeRepresenter.add_representer(list,
                                SafeRepresenter.represent_list)

SafeRepresenter.add_representer(tuple,
                                SafeRepresenter.represent_list)

SafeRepresenter.add_representer(dict,
                                SafeRepresenter.represent_dict)

SafeRepresenter.add_representer(set,
                                SafeRepresenter.represent_set)

SafeRepresenter.add_representer(ordereddict,
                                SafeRepresenter.represent_ordereddict)

SafeRepresenter.add_representer(datetime.date,
                                SafeRepresenter.represent_date)

SafeRepresenter.add_representer(datetime.datetime,
                                SafeRepresenter.represent_datetime)

SafeRepresenter.add_representer(None,
                                SafeRepresenter.represent_undefined)


class Representer(SafeRepresenter):
    if PY2:
        def represent_str(self, data):
            tag = None
            style = None
            try:
                data = unicode(data, 'ascii')
                tag = u'tag:yaml.org,2002:str'
            except UnicodeDecodeError:
                try:
                    data = unicode(data, 'utf-8')
                    tag = u'tag:yaml.org,2002:python/str'
                except UnicodeDecodeError:
                    data = data.encode('base64')
                    tag = u'tag:yaml.org,2002:binary'
                    style = '|'
            return self.represent_scalar(tag, data, style=style)

        def represent_unicode(self, data):
            tag = None
            try:
                data.encode('ascii')
                tag = u'tag:yaml.org,2002:python/unicode'
            except UnicodeEncodeError:
                tag = u'tag:yaml.org,2002:str'
            return self.represent_scalar(tag, data)

        def represent_long(self, data):
            tag = u'tag:yaml.org,2002:int'
            if int(data) is not data:
                tag = u'tag:yaml.org,2002:python/long'
            return self.represent_scalar(tag, to_unicode(data))

    def represent_complex(self, data):
        if data.imag == 0.0:
            data = u'%r' % data.real
        elif data.real == 0.0:
            data = u'%rj' % data.imag
        elif data.imag > 0:
            data = u'%r+%rj' % (data.real, data.imag)
        else:
            data = u'%r%rj' % (data.real, data.imag)
        return self.represent_scalar(u'tag:yaml.org,2002:python/complex', data)

    def represent_tuple(self, data):
        return self.represent_sequence(u'tag:yaml.org,2002:python/tuple', data)

    def represent_name(self, data):
        name = u'%s.%s' % (data.__module__, data.__name__)
        return self.represent_scalar(u'tag:yaml.org,2002:python/name:' +
                                     name, u'')

    def represent_module(self, data):
        return self.represent_scalar(
            u'tag:yaml.org,2002:python/module:'+data.__name__, u'')

    if PY2:
        def represent_instance(self, data):
            # For instances of classic classes, we use __getinitargs__ and
            # __getstate__ to serialize the data.

            # If data.__getinitargs__ exists, the object must be reconstructed
            # by calling cls(**args), where args is a tuple returned by
            # __getinitargs__. Otherwise, the cls.__init__ method should never
            # be called and the class instance is created by instantiating a
            # trivial class and assigning to the instance's __class__ variable.

            # If data.__getstate__ exists, it returns the state of the object.
            # Otherwise, the state of the object is data.__dict__.

            # We produce either a !!python/object or !!python/object/new node.
            # If data.__getinitargs__ does not exist and state is a dictionary,
            # we produce a !!python/object node . Otherwise we produce a
            # !!python/object/new node.

            cls = data.__class__
            class_name = u'%s.%s' % (cls.__module__, cls.__name__)
            args = None
            state = None
            if hasattr(data, '__getinitargs__'):
                args = list(data.__getinitargs__())
            if hasattr(data, '__getstate__'):
                state = data.__getstate__()
            else:
                state = data.__dict__
            if args is None and isinstance(state, dict):
                return self.represent_mapping(
                    u'tag:yaml.org,2002:python/object:'+class_name, state)
            if isinstance(state, dict) and not state:
                return self.represent_sequence(
                    u'tag:yaml.org,2002:python/object/new:' +
                    class_name, args)
            value = {}
            if args:
                value['args'] = args
            value['state'] = state
            return self.represent_mapping(
                u'tag:yaml.org,2002:python/object/new:'+class_name, value)

    def represent_object(self, data):
        # We use __reduce__ API to save the data. data.__reduce__ returns
        # a tuple of length 2-5:
        #   (function, args, state, listitems, dictitems)

        # For reconstructing, we calls function(*args), then set its state,
        # listitems, and dictitems if they are not None.

        # A special case is when function.__name__ == '__newobj__'. In this
        # case we create the object with args[0].__new__(*args).

        # Another special case is when __reduce__ returns a string - we don't
        # support it.

        # We produce a !!python/object, !!python/object/new or
        # !!python/object/apply node.

        cls = type(data)
        if cls in copyreg.dispatch_table:
            reduce = copyreg.dispatch_table[cls](data)
        elif hasattr(data, '__reduce_ex__'):
            reduce = data.__reduce_ex__(2)
        elif hasattr(data, '__reduce__'):
            reduce = data.__reduce__()
        else:
            raise RepresenterError("cannot represent object: %r" % data)
        reduce = (list(reduce)+[None]*5)[:5]
        function, args, state, listitems, dictitems = reduce
        args = list(args)
        if state is None:
            state = {}
        if listitems is not None:
            listitems = list(listitems)
        if dictitems is not None:
            dictitems = dict(dictitems)
        if function.__name__ == '__newobj__':
            function = args[0]
            args = args[1:]
            tag = u'tag:yaml.org,2002:python/object/new:'
            newobj = True
        else:
            tag = u'tag:yaml.org,2002:python/object/apply:'
            newobj = False
        function_name = u'%s.%s' % (function.__module__, function.__name__)
        if not args and not listitems and not dictitems \
                and isinstance(state, dict) and newobj:
            return self.represent_mapping(
                u'tag:yaml.org,2002:python/object:'+function_name, state)
        if not listitems and not dictitems  \
                and isinstance(state, dict) and not state:
            return self.represent_sequence(tag+function_name, args)
        value = {}
        if args:
            value['args'] = args
        if state or not isinstance(state, dict):
            value['state'] = state
        if listitems:
            value['listitems'] = listitems
        if dictitems:
            value['dictitems'] = dictitems
        return self.represent_mapping(tag+function_name, value)

if PY2:
    Representer.add_representer(str,
                                Representer.represent_str)

    Representer.add_representer(unicode,
                                Representer.represent_unicode)

    Representer.add_representer(long,
                                Representer.represent_long)

Representer.add_representer(complex,
                            Representer.represent_complex)

Representer.add_representer(tuple,
                            Representer.represent_tuple)

Representer.add_representer(type,
                            Representer.represent_name)

if PY2:
    Representer.add_representer(types.ClassType,
                                Representer.represent_name)

Representer.add_representer(types.FunctionType,
                            Representer.represent_name)

Representer.add_representer(types.BuiltinFunctionType,
                            Representer.represent_name)

Representer.add_representer(types.ModuleType,
                            Representer.represent_module)

if PY2:
    Representer.add_multi_representer(types.InstanceType,
                                      Representer.represent_instance)

Representer.add_multi_representer(object,
                                  Representer.represent_object)


try:
    from .comments import CommentedMap, CommentedOrderedMap, CommentedSeq, \
        CommentedSet, comment_attrib, merge_attrib
except ImportError:  # for Jython
    from ruamel.yaml.comments import CommentedMap, CommentedOrderedMap, \
        CommentedSeq, CommentedSet, comment_attrib, merge_attrib


class RoundTripRepresenter(SafeRepresenter):
    # need to add type here and write out the .comment
    # in serializer and emitter

    def __init__(self, default_style=None, default_flow_style=None):
        if default_flow_style is None:
            default_flow_style = False
        SafeRepresenter.__init__(self, default_style=default_style,
                                 default_flow_style=default_flow_style)

    def represent_none(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:null',
                                     u'')

    def represent_preserved_scalarstring(self, data):
        tag = None
        style = '|'
        if PY2 and not isinstance(data, unicode):
            data = unicode(data, 'ascii')
        tag = u'tag:yaml.org,2002:str'
        return self.represent_scalar(tag, data, style=style)

    def represent_single_quoted_scalarstring(self, data):
        tag = None
        style = "'"
        if PY2 and not isinstance(data, unicode):
            data = unicode(data, 'ascii')
        tag = u'tag:yaml.org,2002:str'
        return self.represent_scalar(tag, data, style=style)

    def represent_double_quoted_scalarstring(self, data):
        tag = None
        style = '"'
        if PY2 and not isinstance(data, unicode):
            data = unicode(data, 'ascii')
        tag = u'tag:yaml.org,2002:str'
        return self.represent_scalar(tag, data, style=style)

    def represent_sequence(self, tag, sequence, flow_style=None):
        value = []
        # if the flow_style is None, the flow style tacked on to the object
        # explicitly will be taken. If that is None as well the default flow
        # style rules
        try:
            flow_style = sequence.fa.flow_style(flow_style)
        except AttributeError:
            flow_style = flow_style
        try:
            anchor = sequence.yaml_anchor()
        except AttributeError:
            anchor = None
        node = SequenceNode(tag, value, flow_style=flow_style, anchor=anchor)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        try:
            comment = getattr(sequence, comment_attrib)
            item_comments = comment.items
            node.comment = comment.comment
            try:
                node.comment.append(comment.end)
            except AttributeError:
                pass
        except AttributeError:
            item_comments = {}
        for idx, item in enumerate(sequence):
            node_item = self.represent_data(item)
            node_item.comment = item_comments.get(idx)
            if not (isinstance(node_item, ScalarNode) and not node_item.style):
                best_style = False
            value.append(node_item)
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        try:
            flow_style = mapping.fa.flow_style(flow_style)
        except AttributeError:
            flow_style = flow_style
        try:
            anchor = mapping.yaml_anchor()
        except AttributeError:
            anchor = None
        node = MappingNode(tag, value, flow_style=flow_style, anchor=anchor)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        # no sorting! !!
        try:
            comment = getattr(mapping, comment_attrib)
            node.comment = comment.comment
            if node.comment and node.comment[1]:
                for ct in node.comment[1]:
                    ct.reset()
            item_comments = comment.items
            for v in item_comments.values():
                if v and v[1]:
                    for ct in v[1]:
                        ct.reset()
            try:
                node.comment.append(comment.end)
            except AttributeError:
                pass
        except AttributeError:
            item_comments = {}
        for item_key, item_value in mapping.items():
            node_key = self.represent_key(item_key)
            node_value = self.represent_data(item_value)
            item_comment = item_comments.get(item_key)
            if item_comment:
                assert getattr(node_key, 'comment', None) is None
                node_key.comment = item_comment[:2]
                nvc = getattr(node_value, 'comment', None)
                if nvc is not None:  # end comment already there
                    nvc[0] = item_comment[2]
                    nvc[1] = item_comment[3]
                else:
                    node_value.comment = item_comment[2:]
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and not
                    node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        merge_list = [m[1] for m in getattr(mapping, merge_attrib, [])]
        if merge_list:
            # because of the call to represent_data here, the anchors
            # are marked as being used and thereby created
            if len(merge_list) == 1:
                arg = self.represent_data(merge_list[0])
            else:
                arg = self.represent_data(merge_list)
                arg.flow_style = True
            value.insert(0,
                         (ScalarNode(u'tag:yaml.org,2002:merge', '<<'), arg))
        return node

    def represent_omap(self, tag, omap, flow_style=None):
        value = []
        try:
            flow_style = omap.fa.flow_style(flow_style)
        except AttributeError:
            flow_style = flow_style
        try:
            anchor = omap.yaml_anchor()
        except AttributeError:
            anchor = None
        node = SequenceNode(tag, value, flow_style=flow_style, anchor=anchor)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        try:
            comment = getattr(omap, comment_attrib)
            node.comment = comment.comment
            if node.comment and node.comment[1]:
                for ct in node.comment[1]:
                    ct.reset()
            item_comments = comment.items
            for v in item_comments.values():
                if v and v[1]:
                    for ct in v[1]:
                        ct.reset()
            try:
                node.comment.append(comment.end)
            except AttributeError:
                pass
        except AttributeError:
            item_comments = {}
        for item_key in omap:
            item_val = omap[item_key]
            node_item = self.represent_data({item_key: item_val})
            # node item has two scalars in value: node_key and node_value
            item_comment = item_comments.get(item_key)
            if item_comment:
                if item_comment[1]:
                    node_item.comment = [None, item_comment[1]]
                assert getattr(node_item.value[0][0], 'comment', None) is None
                node_item.value[0][0].comment = [item_comment[0], None]
                nvc = getattr(node_item.value[0][1], 'comment', None)
                if nvc is not None:  # end comment already there
                    nvc[0] = item_comment[2]
                    nvc[1] = item_comment[3]
                else:
                    node_item.value[0][1].comment = item_comment[2:]
            # if not (isinstance(node_item, ScalarNode) \
            #    and not node_item.style):
            #     best_style = False
            value.append(node_item)
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_set(self, setting):
        flow_style = False
        tag = u'tag:yaml.org,2002:set'
        # return self.represent_mapping(tag, value)
        value = []
        flow_style = setting.fa.flow_style(flow_style)
        try:
            anchor = setting.yaml_anchor()
        except AttributeError:
            anchor = None
        node = MappingNode(tag, value, flow_style=flow_style, anchor=anchor)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        # no sorting! !!
        try:
            comment = getattr(setting, comment_attrib)
            node.comment = comment.comment
            if node.comment and node.comment[1]:
                for ct in node.comment[1]:
                    ct.reset()
            item_comments = comment.items
            for v in item_comments.values():
                if v and v[1]:
                    for ct in v[1]:
                        ct.reset()
            try:
                node.comment.append(comment.end)
            except AttributeError:
                pass
        except AttributeError:
            item_comments = {}
        for item_key in setting.odict:
            node_key = self.represent_key(item_key)
            node_value = self.represent_data(None)
            item_comment = item_comments.get(item_key)
            if item_comment:
                assert getattr(node_key, 'comment', None) is None
                node_key.comment = item_comment[:2]
            node_key.style = node_value.style = "?"
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and not
                    node_value.style):
                best_style = False
            value.append((node_key, node_value))
        best_style = best_style
        return node

    def represent_dict(self, data):
        """write out tag if saved on loading"""
        try:
            t = data.tag.value
        except AttributeError:
            t = None
        if t:
            while t and t[0] == '!':
                t = t[1:]
            tag = 'tag:yaml.org,2002:' + t
        else:
            tag = u'tag:yaml.org,2002:map'
        return self.represent_mapping(tag, data)


RoundTripRepresenter.add_representer(type(None),
                                     RoundTripRepresenter.represent_none)

RoundTripRepresenter.add_representer(
    PreservedScalarString,
    RoundTripRepresenter.represent_preserved_scalarstring)

RoundTripRepresenter.add_representer(
    SingleQuotedScalarString,
    RoundTripRepresenter.represent_single_quoted_scalarstring)

RoundTripRepresenter.add_representer(
    DoubleQuotedScalarString,
    RoundTripRepresenter.represent_double_quoted_scalarstring)

RoundTripRepresenter.add_representer(CommentedSeq,
                                     RoundTripRepresenter.represent_list)

RoundTripRepresenter.add_representer(CommentedMap,
                                     RoundTripRepresenter.represent_dict)

RoundTripRepresenter.add_representer(CommentedOrderedMap,
                                     RoundTripRepresenter.represent_ordereddict)

if sys.version_info >= (2, 7):
    import collections
    RoundTripRepresenter.add_representer(collections.OrderedDict,
                                         RoundTripRepresenter.represent_ordereddict)

RoundTripRepresenter.add_representer(CommentedSet,
                                     RoundTripRepresenter.represent_set)
