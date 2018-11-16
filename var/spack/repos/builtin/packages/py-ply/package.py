# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPly(PythonPackage):
    """PLY is nothing more than a straightforward lex/yacc implementation."""
    homepage = "http://www.dabeaz.com/ply"
    url      = "http://www.dabeaz.com/ply/ply-3.11.tar.gz"

    version('3.11', '6465f602e656455affcd7c5734c638f8')
    version('3.8', '94726411496c52c87c2b9429b12d5c50')
