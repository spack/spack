# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDoxypypy(PythonPackage):
    """A Doxygen filter for Python.

    A more Pythonic version of doxypy, a Doxygen filter for Python.
    """

    homepage = "https://github.com/Feneric/doxypypy"
    url      = "https://pypi.io/packages/source/d/doxypypy/doxypypy-0.8.8.6.tar.gz"

    version('0.8.8.6', '6b3fe4eff5d459400071b626333fe15f')

    depends_on('py-setuptools', type='build')
