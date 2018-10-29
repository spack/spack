# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFunctools32(PythonPackage):
    """Backport of the functools module from Python 3.2.3 for use on 2.7 and
    PyPy."""

    homepage = "https://github.com/MiCHiLU/python-functools32"
    url      = "https://pypi.io/packages/source/f/functools32/functools32-3.2.3-2.tar.gz"

    version('3.2.3-2', '09f24ffd9af9f6cd0f63cb9f4e23d4b2')
