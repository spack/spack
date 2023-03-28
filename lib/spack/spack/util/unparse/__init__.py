# Copyright (c) 2014-2021, Simon Percivall and Spack Project Developers.
#
# SPDX-License-Identifier: Python-2.0
# coding: utf-8
from __future__ import absolute_import

import io

from .unparser import Unparser

__version__ = "1.6.3"


def unparse(tree, py_ver_consistent=False):
    v = io.StringIO()
    Unparser(py_ver_consistent=py_ver_consistent).visit(tree, v)
    return v.getvalue().strip() + "\n"
