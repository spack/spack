# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBumphunter(RPackage):
    """Bump Hunter.

       Tools for finding bumps in genomic data"""

    homepage = "https://bioconductor.org/packages/bumphunter"
    git      = "https://git.bioconductor.org/packages/bumphunter.git"

    version('1.26.0', commit='606bee8708a0911ced3efb197970b4c9fa52f2fa')
    version('1.24.5', commit='29b874033a38e86103b58ef2d4a55f285758147b')
    version('1.22.0', commit='fb71b193f4ef7fa12d100441e6eb498765f7afde')
    version('1.20.0', commit='c9d8e7ab0c19299988e5d7fa74970312e9a1eac0')
    version('1.16.0', commit='1c3ab4d1fd2d75b1586ccef12665960b3602080a')

    depends_on('r-annotationdbi', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-dorng', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-foreach', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-genomicfeatures', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-genomicranges', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-iranges@2.3.23:', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-iterators', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-limma', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-locfit', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-matrixstats', when='@1.16.0:', type=('build', 'run'))
    depends_on('r@2.10:', when='@1.16.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', when='@1.16.0:', type=('build', 'run'))

    depends_on('r@3.4:', when='@1.20.0:', type=('build', 'run'))

    depends_on('r@3.5:', when='@1.24.5:', type=('build', 'run'))
