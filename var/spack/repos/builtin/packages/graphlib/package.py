# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Graphlib(CMakePackage):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "https://github.com/LLNL/graphlib"
    url      = "https://github.com/LLNL/graphlib/archive/v2.0.0.tar.gz"

    version('2.0.0', '43c6df84f1d38ba5a5dce0ae19371a70')
    version('3.0.0', '625d199f97ab1b84cbc8daabcaee5e2a')

    depends_on('cmake@2.6:', type='build')
