# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAlpine(RPackage):
    """Fragment sequence bias modeling and correction for RNA-seq
    transcript abundance estimation."""

    homepage = "http://bioconductor.org/packages/alpine/"
    git      = "https://git.bioconductor.org/packages/alpine.git"

    version('1.2.0', commit='896872e6071769e1ac2cf786974edb8b875c45eb')

    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r-speedglm', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
