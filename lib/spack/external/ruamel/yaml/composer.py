# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function


try:
    from .error import MarkedYAMLError
    from .compat import utf8
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.error import MarkedYAMLError
    from ruamel.yaml.compat import utf8

from ruamel.yaml.events import (
    StreamStartEvent, StreamEndEvent, MappingStartEvent, MappingEndEvent,
    SequenceStartEvent, SequenceEndEvent, AliasEvent, ScalarEvent,
)
from ruamel.yaml.nodes import (
    MappingNode, ScalarNode, SequenceNode,
)

__all__ = ['Composer', 'ComposerError']


class ComposerError(MarkedYAMLError):
    pass


class Composer(object):
    def __init__(self):
        self.anchors = {}

    def check_node(self):
        # Drop the STREAM-START event.
        if self.check_event(StreamStartEvent):
            self.get_event()

        # If there are more documents available?
        return not self.check_event(StreamEndEvent)

    def get_node(self):
        # Get the root node of the next document.
        if not self.check_event(StreamEndEvent):
            return self.compose_document()

    def get_single_node(self):
        # Drop the STREAM-START event.
        self.get_event()

        # Compose a document if the stream is not empty.
        document = None
        if not self.check_event(StreamEndEvent):
            document = self.compose_document()

        # Ensure that the stream contains no more documents.
        if not self.check_event(StreamEndEvent):
            event = self.get_event()
            raise ComposerError(
                "expected a single document in the stream",
                document.start_mark, "but found another document",
                event.start_mark)

        # Drop the STREAM-END event.
        self.get_event()

        return document

    def compose_document(self):
        # Drop the DOCUMENT-START event.
        self.get_event()

        # Compose the root node.
        node = self.compose_node(None, None)

        # Drop the DOCUMENT-END event.
        self.get_event()

        self.anchors = {}
        return node

    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            event = self.get_event()
            alias = event.anchor
            if alias not in self.anchors:
                raise ComposerError(
                    None, None, "found undefined alias %r"
                    % utf8(alias), event.start_mark)
            return self.anchors[alias]
        event = self.peek_event()
        anchor = event.anchor
        if anchor is not None:  # have an anchor
            if anchor in self.anchors:
                raise ComposerError(
                    "found duplicate anchor %r; first occurence"
                    % utf8(anchor), self.anchors[anchor].start_mark,
                    "second occurence", event.start_mark)
        self.descend_resolver(parent, index)
        if self.check_event(ScalarEvent):
            node = self.compose_scalar_node(anchor)
        elif self.check_event(SequenceStartEvent):
            node = self.compose_sequence_node(anchor)
        elif self.check_event(MappingStartEvent):
            node = self.compose_mapping_node(anchor)
        self.ascend_resolver()
        return node

    def compose_scalar_node(self, anchor):
        event = self.get_event()
        tag = event.tag
        if tag is None or tag == u'!':
            tag = self.resolve(ScalarNode, event.value, event.implicit)
        node = ScalarNode(tag, event.value,
                          event.start_mark, event.end_mark, style=event.style,
                          comment=event.comment)
        if anchor is not None:
            self.anchors[anchor] = node
        return node

    def compose_sequence_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == u'!':
            tag = self.resolve(SequenceNode, None, start_event.implicit)
        node = SequenceNode(tag, [],
                            start_event.start_mark, None,
                            flow_style=start_event.flow_style,
                            comment=start_event.comment, anchor=anchor)
        if anchor is not None:
            self.anchors[anchor] = node
        index = 0
        while not self.check_event(SequenceEndEvent):
            node.value.append(self.compose_node(node, index))
            index += 1
        end_event = self.get_event()
        if node.flow_style is True and end_event.comment is not None:
            if node.comment is not None:
                print('Warning: unexpected end_event commment in sequence '
                      'node {0}'.format(node.flow_style))
            node.comment = end_event.comment
        node.end_mark = end_event.end_mark
        self.check_end_doc_comment(end_event, node)
        return node

    def compose_mapping_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == u'!':
            tag = self.resolve(MappingNode, None, start_event.implicit)
        node = MappingNode(tag, [],
                           start_event.start_mark, None,
                           flow_style=start_event.flow_style,
                           comment=start_event.comment, anchor=anchor)
        if anchor is not None:
            self.anchors[anchor] = node
        while not self.check_event(MappingEndEvent):
            # key_event = self.peek_event()
            item_key = self.compose_node(node, None)
            # if item_key in node.value:
            #     raise ComposerError("while composing a mapping",
            #             start_event.start_mark,
            #             "found duplicate key", key_event.start_mark)
            item_value = self.compose_node(node, item_key)
            # node.value[item_key] = item_value
            node.value.append((item_key, item_value))
        end_event = self.get_event()
        if node.flow_style is True and end_event.comment is not None:
            node.comment = end_event.comment
        node.end_mark = end_event.end_mark
        self.check_end_doc_comment(end_event, node)
        return node

    def check_end_doc_comment(self, end_event, node):
        if end_event.comment and end_event.comment[1]:
            # pre comments on an end_event, no following to move to
            if node.comment is None:
                node.comment = [None, None]
            assert not isinstance(node, ScalarEvent)
            # this is a post comment on a mapping node, add as third element
            # in the list
            node.comment.append(end_event.comment[1])
            end_event.comment[1] = None
