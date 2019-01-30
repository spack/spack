# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVariantannotation(RPackage):
    """Annotate variants, compute amino acid coding changes, predict coding
       outcomes."""

    homepage = "https://www.bioconductor.org/packages/VariantAnnotation/"
    git      = "https://git.bioconductor.org/packages/VariantAnnotation.git"

    version('1.22.3', commit='3a91b6d4297aa416d5f056dec6f8925eb1a8eaee')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-bsgenome', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-genomicfeatures', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.22.3')
