# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AdeptUtils(CMakePackage):
    """Utility libraries for LLNL performance tools."""

    homepage = "https://github.com/llnl/adept-utils"
    url      = "https://github.com/llnl/adept-utils/archive/v1.0.tar.gz"

    version('1.0.1', '731a310717adcb004d9d195130efee7d')
    version('1.0',   '5c6cd9badce56c945ac8551e34804397')

    depends_on('boost')
    depends_on('mpi')
    depends_on('cmake@2.8:', type='build')
