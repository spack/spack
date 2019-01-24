# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGtrellis(RPackage):
    """Genome level Trellis graph visualizes genomic data conditioned by
       genomic categories (e.g. chromosomes). For each genomic category,
       multiple dimensional data which are represented as tracks describe
       different features from different aspects. This package provides high
       flexibility to arrange genomic categories and to add self-defined
       graphics in the plot."""

    homepage = "https://bioconductor.org/packages/gtrellis/"
    git      = "https://git.bioconductor.org/packages/gtrellis.git"

    version('1.8.0', commit='f813b420a008c459f63a2a13e5e64c5507c4c472')

    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-circlize', type=('build', 'run'))
    depends_on('r-getoptlong', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
