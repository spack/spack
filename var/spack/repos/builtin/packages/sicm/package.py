# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sicm(CMakePackage):
    """SICM: Simplified Interface to Complex Memory."""

    homepage = "https://github.com/lanl/SICM/"
    git      = "https://github.com/lanl/SICM.git"

    maintainers = []

    version('master')

    depends_on('jemalloc jemalloc_prefix=je_')
    depends_on('numactl')

    def cmake_args(self):
        return []
