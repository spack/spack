# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This is a fake set of symbols to allow spack to import typing in python
versions where we do not support type checking (<3)
"""
from collections import defaultdict

# (1) Unparameterized types.
IntVar = object
Literal = object
NewType = object
Text = object

# (2) Parameterized types.
Protocol = defaultdict(lambda: object)

# (3) Macro for avoiding evaluation except during type checking.
TYPE_CHECKING = False

# (4) Decorators.
final = lambda x: x
overload = lambda x: x
runtime_checkable = lambda x: x
