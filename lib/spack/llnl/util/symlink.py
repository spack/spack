# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

if sys.platform == "win32":
    from ._windows import islink, symlink
else:
    symlink = os.symlink
    islink = os.path.islink

__all__ = ["symlink", "islink"]
