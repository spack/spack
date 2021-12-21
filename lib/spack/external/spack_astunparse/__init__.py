# coding: utf-8
from __future__ import absolute_import
from six.moves import cStringIO
from .unparser import Unparser


__version__ = '1.6.3'


def unparse(tree, py_ver_consistent=False):
    v = cStringIO()
    Unparser(tree, file=v, py_ver_consistent=py_ver_consistent)
    return v.getvalue()
