# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAdsplit(RPackage):
    """This package implements clustering of microarray gene expression
    profiles according to functional annotations. For each term genes
    are annotated to, splits into two subclasses are computed and a
    significance of the supporting gene set is determined."""

    homepage = "https://www.bioconductor.org/packages/adSplit/"
    git      = "https://git.bioconductor.org/packages/adSplit.git"

    version('1.46.0', commit='7e81a83f34d371447f491b3a146bf6851e260c7c')

    depends_on('r@3.4.0:3.4.9', when='@1.46.0')
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-kegg-db', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
