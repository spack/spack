# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

__all__ = ["ScalarString", "PreservedScalarString", "SingleQuotedScalarString",
           "DoubleQuotedScalarString"]

try:
    from .compat import text_type
except (ImportError, ValueError):  # for Jython
    from ruamel.yaml.compat import text_type


class ScalarString(text_type):
    def __new__(cls, *args, **kw):
        return text_type.__new__(cls, *args, **kw)


class PreservedScalarString(ScalarString):
    def __new__(cls, value):
        return ScalarString.__new__(cls, value)


class SingleQuotedScalarString(ScalarString):
    def __new__(cls, value):
        return ScalarString.__new__(cls, value)


class DoubleQuotedScalarString(ScalarString):
    def __new__(cls, value):
        return ScalarString.__new__(cls, value)


def preserve_literal(s):
    return PreservedScalarString(s.replace('\r\n', '\n').replace('\r', '\n'))


def walk_tree(base):
    """
    the routine here walks over a simple yaml tree (recursing in
    dict values and list items) and converts strings that
    have multiple lines to literal scalars
    """
    from ruamel.yaml.compat import string_types

    if isinstance(base, dict):
        for k in base:
            v = base[k]
            if isinstance(v, string_types) and '\n' in v:
                base[k] = preserve_literal(v)
            else:
                walk_tree(v)
    elif isinstance(base, list):
        for idx, elem in enumerate(base):
            if isinstance(elem, string_types) and '\n' in elem:
                print(elem)
                base[idx] = preserve_literal(elem)
            else:
                walk_tree(elem)
