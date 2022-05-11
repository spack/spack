# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RMemuse(RPackage):
    """Memory Estimation Utilities.

    How much ram do you need to store a 100,000 by 100,000 matrix? How much ram
    is your current R session using? How much ram do you even have?  Learn the
    scintillating answer to these and many more such questions with the
    'memuse' package."""

    cran = "memuse"

    maintainers = ['dorton21']

    version('4.2-1', sha256='f5e9dbaad4efbbfe219a93f446e318a00cad5b294bfc60ca2146eca894b47cf3')
    version('4.1-0', sha256='58d6d1ca5d6bd481f4ed299eff6a9d5660eb0f8db1abe54c49e144093cba72ad')

    depends_on('r@3.0.0:', type=('build', 'run'))
