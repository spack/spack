# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPly(PythonPackage):
    """PLY is nothing more than a straightforward lex/yacc implementation."""
    homepage = "http://www.dabeaz.com/ply"
    url      = "http://www.dabeaz.com/ply/ply-3.11.tar.gz"

    version('3.11', sha256='928c5642612f4710b168d3c49c25f6ece2913a5e8d1c5e37fde5d6162fec3fd2')
    version('3.8', '94726411496c52c87c2b9429b12d5c50', url='http://www.dabeaz.com/ply/ply-3.8.tar.gz')
