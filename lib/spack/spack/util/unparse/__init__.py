# Copyright (c) 2014-2021, Simon Percivall and Spack Project Developers.
#
# SPDX-License-Identifier: Python-2.0
# coding: utf-8

from __future__ import absolute_import

from six.moves import cStringIO

from .unparser import Unparser

__version__ = '1.6.3'


def unparse(tree, py_ver_consistent=False):
    v = cStringIO()
    unparser = Unparser(py_ver_consistent=py_ver_consistent)
    unparser.visit(tree, v)
    return v.getvalue().strip() + "\n"
