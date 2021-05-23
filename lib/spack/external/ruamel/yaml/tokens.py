# # header
# coding: utf-8


class Token(object):
    def __init__(self, start_mark, end_mark):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        attributes = [key for key in self.__dict__
                      if not key.endswith('_mark')]
        attributes.sort()
        arguments = ', '.join(['%s=%r' % (key, getattr(self, key))
                               for key in attributes])
        return '%s(%s)' % (self.__class__.__name__, arguments)

    def add_post_comment(self, comment):
        if not hasattr(self, '_comment'):
            self._comment = [None, None]
        self._comment[0] = comment

    def add_pre_comments(self, comments):
        if not hasattr(self, '_comment'):
            self._comment = [None, None]
        assert self._comment[1] is None
        self._comment[1] = comments

    def get_comment(self):
        return getattr(self, '_comment', None)

    @property
    def comment(self):
        return getattr(self, '_comment', None)

    def move_comment(self, target):
        """move a comment from this token to target (normally next token)
        used to combine e.g. comments before a BlockEntryToken to the
        ScalarToken that follows it
        """
        c = self.comment
        if c is None:
            return
        # don't push beyond last element
        if isinstance(target, StreamEndToken):
            return
        delattr(self, '_comment')
        tc = target.comment
        if not tc:  # target comment, just insert
            target._comment = c
            return self
        if c[0] and tc[0] or c[1] and tc[1]:
            raise NotImplementedError('overlap in comment %r %r' % c, tc)
        if c[0]:
            tc[0] = c[0]
        if c[1]:
            tc[1] = c[1]
        return self

    def split_comment(self):
        """ split the post part of a comment, and return it
        as comment to be added. Delete second part if [None, None]
         abc:  # this goes to sequence
           # this goes to first element
           - first element
        """
        comment = self.comment
        if comment is None or comment[0] is None:
            return None  # nothing to do
        ret_val = [comment[0], None]
        if comment[1] is None:
            delattr(self, '_comment')
        return ret_val


# class BOMToken(Token):
#     id = '<byte order mark>'

class DirectiveToken(Token):
    id = '<directive>'

    def __init__(self, name, value, start_mark, end_mark):
        Token.__init__(self, start_mark, end_mark)
        self.name = name
        self.value = value


class DocumentStartToken(Token):
    id = '<document start>'


class DocumentEndToken(Token):
    id = '<document end>'


class StreamStartToken(Token):
    id = '<stream start>'

    def __init__(self, start_mark=None, end_mark=None, encoding=None):
        Token.__init__(self, start_mark, end_mark)
        self.encoding = encoding


class StreamEndToken(Token):
    id = '<stream end>'


class BlockSequenceStartToken(Token):
    id = '<block sequence start>'


class BlockMappingStartToken(Token):
    id = '<block mapping start>'


class BlockEndToken(Token):
    id = '<block end>'


class FlowSequenceStartToken(Token):
    id = '['


class FlowMappingStartToken(Token):
    id = '{'


class FlowSequenceEndToken(Token):
    id = ']'


class FlowMappingEndToken(Token):
    id = '}'


class KeyToken(Token):
    id = '?'


class ValueToken(Token):
    id = ':'


class BlockEntryToken(Token):
    id = '-'


class FlowEntryToken(Token):
    id = ','


class AliasToken(Token):
    id = '<alias>'

    def __init__(self, value, start_mark, end_mark):
        Token.__init__(self, start_mark, end_mark)
        self.value = value


class AnchorToken(Token):
    id = '<anchor>'

    def __init__(self, value, start_mark, end_mark):
        Token.__init__(self, start_mark, end_mark)
        self.value = value


class TagToken(Token):
    id = '<tag>'

    def __init__(self, value, start_mark, end_mark):
        Token.__init__(self, start_mark, end_mark)
        self.value = value


class ScalarToken(Token):
    id = '<scalar>'

    def __init__(self, value, plain, start_mark, end_mark, style=None):
        Token.__init__(self, start_mark, end_mark)
        self.value = value
        self.plain = plain
        self.style = style


class CommentToken(Token):
    id = '<comment>'

    def __init__(self, value, start_mark, end_mark):
        Token.__init__(self, start_mark, end_mark)
        self.value = value

    def reset(self):
        if hasattr(self, 'pre_done'):
            delattr(self, 'pre_done')
