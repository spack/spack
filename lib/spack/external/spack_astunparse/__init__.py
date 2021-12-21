# coding: utf-8
from __future__ import absolute_import
from six.moves import cStringIO
from .unparser import Unparser


__version__ = '1.6.3'


def unparse(tree):
    v = cStringIO()
    Unparser(tree, file=v)
    return v.getvalue()
