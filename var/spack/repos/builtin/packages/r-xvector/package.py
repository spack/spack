# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXvector(RPackage):
    """Memory efficient S4 classes for storing sequences "externally" (behind
       an R external pointer, or on disk)."""

    homepage = "https://bioconductor.org/packages/XVector/"
    git      = "https://git.bioconductor.org/packages/XVector.git"

    version('0.20.0', commit='a83a7ea01f6a710f0ba7d9fb021cfa795b291cb4')
    version('0.16.0', commit='54615888e1a559da4a81de33e934fc0f1c3ad99f')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.19.2:', when='@0.20.0', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.24:', when='@0.20.0', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.16:', when='@0.20.0', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@0.16.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@0.20.0', type=('build', 'run'))
