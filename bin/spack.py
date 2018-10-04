#!/usr/bin/env python
#
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Spack uses `python -S` as an interpreter to avoid the issue reported in:
#
# https://github.com/spack/spack/issues/9206
#
# Unfortunately not running `import site` by default causes all sort of
# inconsistencies as:
#
# - the system built-in modules that get linked into a virtual-env differ
#   among python versions and might not include `__future__` or `inpect`
#   (this means that `python -S` might prevent importing those modules)
#
# - the `site.py` used in Python 2.7 virtual environments is that of Python 2.6
#   (https://github.com/pypa/virtualenv/issues/355)
#
# The hack below is needed to restore built-in modules from the system if
# they are missing. It assumes that the module `re` is always present as a
# built-in, and adds its real path to the end of `sys.path` to recover all
# the other system modules.
try:
    import __future__  # noqa
    import inspect  # noqa
except ImportError:
    # If `__future__` is not there, it's very likely we are within
    # a Python 2.7 virtual environment. If `inspect` is not there
    # it could be a Python 3.6 virtual environment.
    import os.path
    import re
    import sys
    re_realpath = os.path.realpath(re.__file__.replace('.pyc', '.py'))
    sys.path.append(os.path.dirname(re_realpath))

import os
import sys

if sys.version_info[:2] < (2, 6):
    v_info = sys.version_info[:3]
    sys.exit("Spack requires Python 2.6 or higher."
             "This is Python %d.%d.%d." % v_info)

# Find spack's location and its prefix.
spack_file = os.path.realpath(os.path.expanduser(__file__))
spack_prefix = os.path.dirname(os.path.dirname(spack_file))

# Allow spack libs to be imported in our scripts
spack_lib_path = os.path.join(spack_prefix, "lib", "spack")
sys.path.insert(0, spack_lib_path)

# Add external libs
spack_external_libs = os.path.join(spack_lib_path, "external")

if sys.version_info[:2] == (2, 6):
    sys.path.insert(0, os.path.join(spack_external_libs, 'py26'))

sys.path.insert(0, spack_external_libs)

# Once we've set up the system path, run the spack main method
import spack.main  # noqa
sys.exit(spack.main.main())
