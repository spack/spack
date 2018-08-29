# coding: utf-8

"""
some helper functions that might be generally useful
"""

from __future__ import print_function
from __future__ import absolute_import

from .compat import text_type, binary_type
from .main import round_trip_load


# originally as comment
# https://github.com/pre-commit/pre-commit/pull/211#issuecomment-186466605
# if you use this in your code, I suggest adding a test in your test suite
# that check this routines output against a known piece of your YAML
# before upgrades to this code break your round-tripped YAML
def load_yaml_guess_indent(stream, **kw):
    """guess the indent and block sequence indent of yaml stream/string

    returns round_trip_loaded stream, indent level, block sequence indent
    - block sequence indent is the number of spaces before a dash relative to previous indent
    - if there are no block sequences, indent is taken from nested mappings, block sequence
      indent is unset (None) in that case
    """
    # load a yaml file guess the indentation, if you use TABs ...
    def leading_spaces(l):
        idx = 0
        while idx < len(l) and l[idx] == ' ':
            idx += 1
        return idx

    if isinstance(stream, text_type):
        yaml_str = stream
    elif isinstance(stream, binary_type):
        yaml_str = stream.decode('utf-8')  # most likely, but the Reader checks BOM for this
    else:
        yaml_str = stream.read()
    map_indent = None
    indent = None  # default if not found for some reason
    block_seq_indent = None
    prev_line_key_only = None
    key_indent = 0
    for line in yaml_str.splitlines():
        rline = line.rstrip()
        lline = rline.lstrip()
        if lline.startswith('- '):
            l_s = leading_spaces(line)
            block_seq_indent = l_s - key_indent
            idx = l_s + 1
            while line[idx] == ' ':  # this will end as we rstripped
                idx += 1
            if line[idx] == '#':     # comment after -
                continue
            indent = idx - key_indent
            break
        if map_indent is None and prev_line_key_only is not None and rline:
            idx = 0
            while line[idx] in ' -':
                idx += 1
            if idx > prev_line_key_only:
                map_indent = idx - prev_line_key_only
        if rline.endswith(':'):
            key_indent = leading_spaces(line)
            idx = 0
            while line[idx] == ' ':  # this will end on ':'
                idx += 1
            prev_line_key_only = idx
            continue
        prev_line_key_only = None
    if indent is None and map_indent is not None:
        indent = map_indent
    return round_trip_load(yaml_str, **kw), indent, block_seq_indent


def configobj_walker(cfg):
    """
    walks over a ConfigObj (INI file with comments) generating
    corresponding YAML output (including comments
    """
    from configobj import ConfigObj
    assert isinstance(cfg, ConfigObj)
    for c in cfg.initial_comment:
        if c.strip():
            yield c
    for s in _walk_section(cfg):
        if s.strip():
            yield s
    for c in cfg.final_comment:
        if c.strip():
            yield c


def _walk_section(s, level=0):
    from configobj import Section
    assert isinstance(s, Section)
    indent = u'  ' * level
    for name in s.scalars:
        for c in s.comments[name]:
            yield indent + c.strip()
        x = s[name]
        if u'\n' in x:
            i = indent + u'  '
            x = u'|\n' + i + x.strip().replace(u'\n', u'\n' + i)
        elif ':' in x:
            x = u"'" + x.replace(u"'", u"''") + u"'"
        line = u'{0}{1}: {2}'.format(indent, name, x)
        c = s.inline_comments[name]
        if c:
            line += u' ' + c
        yield line
    for name in s.sections:
        for c in s.comments[name]:
            yield indent + c.strip()
        line = u'{0}{1}:'.format(indent, name)
        c = s.inline_comments[name]
        if c:
            line += u' ' + c
        yield line
        for val in _walk_section(s[name], level=level+1):
            yield val

# def config_obj_2_rt_yaml(cfg):
#     from .comments import CommentedMap, CommentedSeq
#     from configobj import ConfigObj
#     assert isinstance(cfg, ConfigObj)
#     #for c in cfg.initial_comment:
#     #    if c.strip():
#     #        pass
#     cm = CommentedMap()
#     for name in s.sections:
#         cm[name] = d = CommentedMap()
#
#
#     #for c in cfg.final_comment:
#     #    if c.strip():
#     #        yield c
#     return cm
