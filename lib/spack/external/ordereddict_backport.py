# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This file dispatches to the correct implementation of OrderedDict."""

# TODO: this file, along with py26/ordereddict.py, can be removed when
# TODO: support for python 2.6 will be dropped

# Removing this import will make python 2.6
# fail on import of ordereddict
from __future__ import absolute_import

import sys

if sys.version_info[:2] == (2, 6):
    import ordereddict
    OrderedDict = ordereddict.OrderedDict
else:
    import collections
    OrderedDict = collections.OrderedDict
