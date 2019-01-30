# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRope(PythonPackage):
    """a python refactoring library."""

    homepage = "https://github.com/python-rope/rope"
    url      = "https://pypi.io/packages/source/r/rope/rope-0.10.5.tar.gz"

    version('0.10.5', '21882fd7c04c29d09f75995d8a088be7')

    depends_on('py-setuptools', type='build')
