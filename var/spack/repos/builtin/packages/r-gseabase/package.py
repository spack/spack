# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGseabase(RPackage):
    """This package provides classes and methods to support Gene
    Set Enrichment Analysis (GSEA)."""

    homepage = "https://www.bioconductor.org/packages/GSEABase/"
    git      = "https://git.bioconductor.org/packages/GSEABase.git"

    version('1.38.2', commit='84c9f10c316163118ca990900a7a67555b96e75b')

    depends_on('r@3.4.0:3.4.9', when='@1.38.2')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
