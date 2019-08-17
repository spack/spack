# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMpmath(PythonPackage):
    """A Python library for arbitrary-precision floating-point arithmetic."""
    homepage = "http://mpmath.org"
    url      = "https://pypi.io/packages/source/m/mpmath/mpmath-1.0.0.tar.gz"

    version('1.1.0', sha256='fc17abe05fbab3382b61a123c398508183406fa132e0223874578e20946499f6')
    version('1.0.0', '998f10cb231af62743212ca80693f1b5')
    version('0.19', 'af5cc956b2673b33a25c3e57299bae7b')
