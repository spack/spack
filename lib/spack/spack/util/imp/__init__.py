# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Consolidated module for all imports done by Spack.

Many parts of Spack have to import Python code. This utility package
wraps Spack's interface with Python's import system.

We do this because Python's import system is confusing and changes from
Python version to Python version, and we should be able to adapt our
approach to the underlying implementation.

Currently, this uses ``importlib.machinery`` where available and ``imp``
when ``importlib`` is not completely usable.
"""

try:
    from .importlib_importer import load_source  # noqa
except ImportError:
    from .imp_importer import load_source        # noqa
