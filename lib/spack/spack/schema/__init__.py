# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains jsonschema files for all of Spack's YAML formats.
"""
from llnl.util.lang import list_modules

# Automatically bring in all sub-modules
__all__ = []
for mod in list_modules(__path__[0]):
    __import__('%s.%s' % (__name__, mod))
    __all__.append(mod)
