# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiovizbase(RPackage):
    """The biovizBase package is designed to provide a set of
    utilities, color schemes and conventions for genomic data.
    It serves as the base for various high-level packages for
    biological data visualization. This saves development effort
    and encourages consistency."""

    homepage = "http://bioconductor.org/packages/biovizBase/"
    git      = "https://git.bioconductor.org/packages/biovizBase.git"

    version('1.24.0', commit='ae9cd2ff665b74a8f45ed9c1d17fc0a778b4af6c')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dichromat', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-ensembldb', type=('build', 'run'))
    depends_on('r-annotationfilter', type=('build', 'run'))
