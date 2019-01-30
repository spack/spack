# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBumphunter(RPackage):
    """Tools for finding bumps in genomic data"""

    homepage = "http://bioconductor.org/packages/bumphunter/"
    git      = "https://git.bioconductor.org/packages/bumphunter.git"

    version('1.16.0', commit='1c3ab4d1fd2d75b1586ccef12665960b3602080a')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-dorng', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.0')
